import osgeo.gdal as gdal
import osgeo.osr as osr
import errno
import os

# importing system-specific modules
try:
    import crs as osge_c
except ModuleNotFoundError:
    import osgeo_easy.crs as osge_c

DEFAULT_NODATA = -999

__FILEEXT_DRIVER = {
    "tif": "GTiff",
    "tiff": "GTiff",
    "geotiff": "GTiff",
    "bil": "EHdr"
}


def get_dataset(raster_ref) -> gdal.Dataset:
    """
    Always return a gdal.Dataset
    :param raster_ref: String (raster file path) or gdal.Dataset
    :return:
    """
    if isinstance(raster_ref, str):
        return read(raster_ref)
    elif isinstance(raster_ref, gdal.Dataset):
        return raster_ref
    else:
        raise TypeError


def get_epsg(ref) -> int:
    """

    :param ref: File path or ogr.DataSource or osr.SpatialReference
    :return:
    """
    if isinstance(ref, str) or isinstance(ref, gdal.Dataset):
        return int(get_spatial_reference(ref).GetAttrValue("AUTHORITY", 1))
    elif isinstance(ref, osr.SpatialReference):
        return ref.GetAttrValue("AUTHORITY", 1)
    elif isinstance(ref, int):
        return ref
    else:
        raise TypeError


def fill_crs_if_needed(raster_ref, output_crs: int=osge_c.DEFAULT_EPSG) -> gdal.Dataset:
    """

    :param raster_ref:
    :param output_crs:
    :return:
    """

    raster_ds = get_dataset(raster_ref)
    inp_raster_proj = raster_ds.GetProjection()

    # if already set a crs, does nothing
    if (inp_raster_proj is not None) and (inp_raster_proj.strip() != ""):
        return raster_ds
    else:
        del inp_raster_proj

    # get spatial reference
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(output_crs)
    raster_ds.SetProjection(srs.ExportToWkt())

    return raster_ds


def get_spatial_reference(raster_ref) -> osr.SpatialReference:
    """

    :param raster_ref:
    :return:
    """

    raster_ds = get_dataset(raster_ref)
    raster_proj = raster_ds.GetProjection()
    raster_sr = osr.SpatialReference(wkt=raster_proj)

    return raster_sr


def read(file_path: str) -> gdal.Dataset:
    """
    Just overloads osgeo.ogr.Open following PEP-8 standards
    :param file_path:
    :return:
    """

    ret = gdal.Open(file_path)
    if ret is None:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
    return ret


def reproject(raster_ref, output_crs, output_file: str=None) -> gdal.Dataset:
    """

    :param raster_ref:
    :param output_crs:
    :param output_file:
    :return:
    """

    rst_ds = get_dataset(raster_ref)
    rst_ds = fill_crs_if_needed(rst_ds)
    inp_epsg, out_epsg = get_epsg(rst_ds), get_epsg(output_crs)

    # check if reprojection is unnecessary
    if inp_epsg == out_epsg:
        if output_file is not None:
            # TODO
            raise NotImplemented("Feature for saving a reprojected raster.")
        return rst_ds

    raise NotImplementedError("Effective reprojection of raster.")


def write(raster_ds: gdal.Dataset, file_path: str) -> None:
    """ Write dataset into a raster file. Abstract the process of getting a GDAL driver """
    driver = __get_driver(file_path)
    driver.CreateCopy(file_path, raster_ds)
    return None


def __get_driver(file_path: str) -> gdal.Driver:
    """

    :param file_path:
    :return:
    """

    splitted = os.path.splitext(file_path)
    if len(splitted) <= 1:
        raise TypeError("Unable to save file without extension (%s)." % file_path)

    file_ext = splitted[-1][1:].lower()
    if file_ext not in __FILEEXT_DRIVER.keys():
        raise TypeError("Unable to finda a driver for file extension '%s'." % file_ext)

    return gdal.GetDriverByName(__FILEEXT_DRIVER[file_ext])
