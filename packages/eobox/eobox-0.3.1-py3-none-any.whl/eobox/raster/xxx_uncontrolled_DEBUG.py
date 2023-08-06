src_file = "/media/ben/AO/phd/01_eodata/preprocessed/s1ms_ms_10m/33UUU_2017/VH/VH_02K0001_20170102T165141_S1B_db.tif"
dst_file = "/home/ben/Desktop/33UUU_2017/VH/VH_02K0001_20170102T165141_S1B_db.tif"
template_file = "/media/ben/AO/phd/01_eodata/readytouse/s2__33UUU_2017__2w__ndvi__vts/33UUU_2017/s2_uuu33_vts2w_2017-01-01_ndvi.tif"


from eobox.raster import gdalutils

gdalutils.reproject_on_template_raster(
    src_file, dst_file, template_file, resampling="near", compress="deflate"
)


# from pathlib import Path
# import pandas as pd
# import rasterio as rio
# import numpy as np
# from glob import glob
# import os
# from osgeo import gdal
# from tqdm import tqdm
# import subprocess

# from eobox.raster import cube
# from eobox.raster import gdalutils

# from eobox.raster.utils import cleanup_df_values_for_given_dtype
# from eobox.raster.utils import dtype_checker_df

# from agrotools import configs

# prjconf = configs.ProjectConfigParser(config_file=None)

# src_ms = prjconf.get_path('EOdata', 'preprocessed')
# dst_ms = prjconf.get_path('EOdata', 'readytouse')

# src_ms_vv =  Path(src_ms / 's1ms_ms_10m/33UUU_2017/VV')
# src_ms_vh =  Path(src_ms / 's1ms_ms_10m/33UUU_2017/VH')

# dst_ms_vv = Path(dst_ms / 's1ms__33UUU_2017__2w__VV__median')
# dst_ms_vh = Path(dst_ms / 's1ms__33UUU_2017__2w__VH__median')

# assert src_ms_vv.exists() & src_ms_vh.exists()

# list_vv = list(src_ms_vv.glob("**/VV_08K0001_*S1[A,B]_db.tif"))
# list_vh = list(src_ms_vh.glob("**/VH_02K0001_*S1[A,B]_db.tif"))
# print("Number of scenes for processing: ", (len(list_vv) + len(list_vh)))
# print(list_vv[:3])
# print(list_vh[:3])
# list_vvvh = (list_vh + list_vv)
# print(len(list_vvvh))

# dct ={}

# for scene in list_vvvh:
#     splitted_stems = scene.stem.split('_')
#     dct[scene] = [scene, scene.stem, splitted_stems[0], splitted_stems[2], splitted_stems[3]]
# df_vvvh = pd.DataFrame.from_dict(dct).T.reset_index(drop=True).rename(columns={0:'path', 1:'uname', 2:'polarization', 3:'date', 4:'sensor'})
# df_vvvh['date'] = pd.to_datetime(df_vvvh['date'].str[:-7])
# df_vvvh['week_number'] =  df_vvvh['date'].dt.week
# df_vvvh['path'] =  df_vvvh['path'].astype(np.str)
# df_vvvh = df_vvvh.sort_values('date')

# print(df_vvvh.shape)

# biweekly_index = pd.date_range(start='2017-01-01', end='2017-12-31', freq='2W')
# df_vvvh['biweek_number'] = 0

# for i in range(0, 27, 1):
#     if i == 26:
#         break
#     else:
#         df_vvvh.loc[(df_vvvh['date'] > biweekly_index[i]) & (df_vvvh['date'] <= biweekly_index[i+1]), ['biweek_number']] = i+1

# assert df_vvvh.week_number.values.max() == 52
# assert df_vvvh.biweek_number.values.max() == 26

# df_vv = df_vvvh[df_vvvh['polarization']=='VV']
# df_vh = df_vvvh[df_vvvh['polarization']=='VH']

# assert df_vv.shape == df_vh.shape

# biweekly_vv = list(df_vv.groupby('biweek_number')['path'].apply(list))
# biweekly_vh = list(df_vh.groupby('biweek_number')['path'].apply(list))

# df_tmp = df_vh[df_vvvh['biweek_number']==1]

# #import rasterio
# #for i in range(df_tmp.shape[0]):
# #    with rasterio.open(df_tmp.path.iloc[0]) as src:
# #        print(src.meta["width"], src.meta["height"])

# # eoc._mrio.windows

# df_l = df_tmp.reset_index(drop=True)

# eoc = cube.EOCube(df_layers=df_l.loc[[5,6], :], chunksize=2**11)
# dst_paths = ["/home/ben/Desktop/a_median_dir/a_median.vrt"]

# ji = 1

# eoc_chunk = eoc.get_chunk(ji=ji)
# eoc_chunk = eoc_chunk.read_data()
# eoc_chunk.data.shape[0] * eoc_chunk.data.shape[1] == eoc_chunk._width * eoc_chunk._height
