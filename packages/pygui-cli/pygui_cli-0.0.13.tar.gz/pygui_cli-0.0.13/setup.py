import json
import platform

from setuptools import setup, find_packages
import os

VERSION = '0.0.13'
NAME = "pygui_cli"

with open("README.md") as fp:
    long_description = fp.read()

setup(name=NAME,
      version=VERSION,
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python、PyQt5、template',
      author='Lin JH',
      author_email='625781186@qq.com',
      url='https://github.com/625781186/pygui_cli',
      license='GPL-3.0',
      description="pyqt5 & pyside2 template.",
      long_description=long_description,
      long_description_content_type='text/markdown',  # This is important
      # --------------------------------------------#
      # package_dir={'source': ''},
      packages=find_packages(),
      # include_package_data=True,  # 和下面的写法冲突

      package_data={
          "": ["*"],
      },

      zip_safe=False,
      install_requires=[
          'docopt',
      ],
      # copy .py file to python's Srcipts
      scripts=[],
      entry_points={
          'console_scripts': [
              'pygui_cli = source.template_cli.tpl:main'
          ]
      },

      )

# import distutils.sysconfig

# PY_SITE_PACKAGES = distutils.sysconfig.get_python_lib(True)
# CONFIG_FILE_NAME = "~\\pip\\{}.json".format(NAME) if ("Windows" in platform.system()) else "~/.pip/{}.json".format(NAME)
# CONFIG_FILE_PATH = os.path.expanduser(CONFIG_FILE_NAME)
# CONFIG_DIR_PATH = os.path.dirname(CONFIG_FILE_PATH)
# if not os.path.exists(CONFIG_DIR_PATH):
    # os.mkdir(CONFIG_DIR_PATH)
## tpl-1.0.0-py3.6.egg
# PY = platform.python_version()  # 3.6.4
# EGG_NAME = NAME + "-" + VERSION + "-" + "py%s" % (str(PY)[:3]) + ".egg"
# EGG_DIR_PATH = os.path.join(PY_SITE_PACKAGES, EGG_NAME, )
# EGG_PATH = os.path.join(EGG_DIR_PATH, "source")

# with open(CONFIG_FILE_PATH, "w", encoding='utf8') as f:
    # f.write(json.dumps(
        # {"source_path": EGG_PATH},
        # ensure_ascii=False,
        # indent=4))
