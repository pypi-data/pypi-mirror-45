# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['niwidgets']

package_data = \
{'': ['*'], 'niwidgets': ['data/*', 'data/example_surfaces/*']}

install_requires = \
['ipyvolume>=0.5.1,<0.6.0',
 'ipywidgets>=7.4,<8.0',
 'matplotlib>=3.0,<4.0',
 'nibabel>=2.4,<3.0',
 'nilearn>=0.5.2,<0.6.0',
 'numpy>=1.16,<2.0',
 'scikit-learn>=0.20.3,<0.21.0',
 'scipy>=1.2,<2.0']

setup_kwargs = {
    'name': 'niwidgets',
    'version': '0.2.2',
    'description': "'Interactive jupyter widgets for neuroimaging.'",
    'long_description': '# Neuroimaging Widgets (`niwidgets`)\n\nThis repository is supposed to provide easy and general wrappers to display\ninteractive widgets that visualise standard-format neuroimaging data, using new\nfunctions and standard functions from other libraries. It looks like this:\n\n![](https://thumbs.gfycat.com/ExcitableReflectingLcont-size_restricted.gif)\n\nInstall via:\n\n```\npip install niwidgets\n```\n\nOr, to get the most up-to-date development version from github:\n\n```\npip install git+git://github.com/nipy/niwidgets/\n```\n\nIt requires nibabel and nilearn:\n\n```\npip install nibabel nilearn\n```\n\nCheck out the examples using the code in this notebook here:\nhttps://github.com/nipy/niwidgets/blob/master/index.ipynb (you need to run the\nnotebook on your local machine to use the interactive features).\n\nor using binder here:\nhttps://mybinder.org/v2/gh/nipy/niwidgets/master?filepath=index.ipynb\n\n### Usage:\n\nThere are currently three supported widgets:\n\n1. Volume widgets. This widget is primarily designed to mimic existing tools\nsuch as <add tool here>, but it also allows you to wrap plots from the `nilearn`\nplotting library to make them interactive.\n\n2. Surface widgets. This widget takes freesurfer-generated volume files and\nturns them into widgets using the `ipyvolume` library. It allows you to add\ndifferent overlays for the surface files.\n\n3. Streamline widgets. This widget accepts `.trk` files and displays the tracts\nusing `ipyvolume`.\n\nTo see how to use these widgets, please check the\n[documentation](nipy.org/niwidgets).\n\nAs an example of how you might generate a Volume widget:\n\n```\nfrom niwidgets import NiftiWidget\n\nmy_widget = NiftiWidget(\'./path/to/file.nii\')\n```\n\nYou can then create a plot either with the default nifti plotter:\n\n```\nmy_widget.nifti_plotter()\n```\n\nThis will give you sliders to slice through the image, and an option to set the\ncolormap.\n\nYou can also provide your own plotting function:\n\n```\nimport nilearn.plotting as nip\n\nmy_widget.nifti_plotter(plotting_func=nip.plot_glass_brain)\n```\n\nBy default, this will give you the following interactive features: -\nselecting a colormap - if supported by the plotting function, x-y-x\nsliders (e.g. for `nip.plot_img`)\n\n\nYou can, however, always provide features you would like to have interactive\nyourself. This follows the normal ipywidgets format. For example, if you provide\na list of strings for a keyword argument, this becomes a drop-down menu. If you\nprovide a tuple of two numbers, this becomes a slider. Take a look at some\nexamples we have in [this\nnotebook](https://github.com/janfreyberg/niwidgets/blob/master/visualisation_wrapper.ipynb)\n(you need to run the notebook on your local machine to use the interactive\nfeatures).\n\nHopefully we will be able to add more default interactive features in the\nfuture, as well as plotting of other data (such as surface projections). If you\nhave any suggestions for plot features to be added, please let us know - or add\nthem yourself and create a pull request!\n\n## Development\n\n![](https://travis-ci.org/nipy/niwidgets.svg?branch=master)\n\n### Contributing\n\nPlease contribute! When writing new widgets, please make sure you include\nexample data that allows users to try a widget without having to munge their\ndata into the right format first.\n\nPlease also make sure you write a test for your new widget. It\'s hard to test\njupyter widgets, but it would be great if you could at least write a test that\n"instantiates" a widget. This allows us to maintain a stable release.\n\n### Development installation\n\nAs always with pip packages, you can install a _"development"_ version of this\npackage by cloning the git repository and installing it via `pip install -e\n/path/to/package`.\n\n### Updating the documentation\n\nTo update the documentation, you can do the following things:\n\n- Make your changes on a separate branch, such as DOC/update-api-documentation.\n- Merge your branch into master Make sure you have the packages in\n- `doc-requirements.txt` installed Run `make gh-pages` in the root directory of\n- the repository\n\nThis should run sphinx to generate the documentation, push it to the gh-pages\nbranch, and then revert to master.\n\n---\n\n_Developed by [Jan Freyberg](http://www.twitter.com/janfreyberg), [Bjoern\nSoergel](http://www.ast.cam.ac.uk/~bs538/), [Satrajit\nGhosh](https://github.com/satra), [Melanie\nGanz](https://github.com/melanieganz), [Murat\nBilgel](https://github.com/bilgelm), [Ariel Rokem](https://github.com/arokem),\nand [elyb01](https://github.com/elyb01)._\n',
    'author': 'Jan Freyberg',
    'author_email': 'jan.freyberg@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
