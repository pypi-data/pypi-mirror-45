# version info for supy

from supy_driver import __version__ as sd_ver
ver_milestone = 2019
ver_major = 4
ver_minor = 17
ver_remark = ''
__version__ = '{ver_milestone}.{ver_major}.{ver_minor}{ver_remark}'.format(
    ver_milestone=ver_milestone,
    ver_major=ver_major,
    ver_minor=ver_minor,
    ver_remark=ver_remark,
)

__version_driver__ = sd_ver
