# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['gaphor',
 'gaphor.UML',
 'gaphor.UML.tests',
 'gaphor.adapters',
 'gaphor.adapters.actions',
 'gaphor.adapters.actions.tests',
 'gaphor.adapters.classes',
 'gaphor.adapters.classes.tests',
 'gaphor.adapters.components',
 'gaphor.adapters.components.tests',
 'gaphor.adapters.interactions',
 'gaphor.adapters.interactions.tests',
 'gaphor.adapters.profiles',
 'gaphor.adapters.profiles.tests',
 'gaphor.adapters.states',
 'gaphor.adapters.states.tests',
 'gaphor.adapters.tests',
 'gaphor.adapters.usecases',
 'gaphor.adapters.usecases.tests',
 'gaphor.diagram',
 'gaphor.diagram.actions',
 'gaphor.diagram.classes',
 'gaphor.diagram.classes.tests',
 'gaphor.diagram.components',
 'gaphor.diagram.components.tests',
 'gaphor.diagram.profiles',
 'gaphor.diagram.states',
 'gaphor.diagram.states.tests',
 'gaphor.diagram.tests',
 'gaphor.misc',
 'gaphor.plugins',
 'gaphor.plugins.alignment',
 'gaphor.plugins.checkmetamodel',
 'gaphor.plugins.diagramlayout',
 'gaphor.plugins.diagramlayout.tests',
 'gaphor.plugins.liveobjectbrowser',
 'gaphor.plugins.pynsource',
 'gaphor.plugins.xmiexport',
 'gaphor.services',
 'gaphor.services.tests',
 'gaphor.storage',
 'gaphor.storage.tests',
 'gaphor.tests',
 'gaphor.tools',
 'gaphor.ui',
 'gaphor.ui.pixmaps',
 'gaphor.ui.tests']

package_data = \
{'': ['*'], 'gaphor.diagram.actions': ['tests/*'], 'gaphor.misc': ['tests/*']}

install_requires = \
['PyGObject>=3.30,<4.0',
 'gaphas>=1.0.0,<2.0.0',
 'pycairo>=1.16,<2.0',
 'zope.component>=4.5,<5.0']

entry_points = \
{'console_scripts': ['gaphor = gaphor:main',
                     'gaphorconvert = gaphor.tools.gaphorconvert:main'],
 'gaphor.services': ['action_manager = '
                     'gaphor.services.actionmanager:ActionManager',
                     'adapter_loader = '
                     'gaphor.services.adapterloader:AdapterLoader',
                     'alignment = gaphor.plugins.alignment:Alignment',
                     'component_registry = '
                     'gaphor.services.componentregistry:ZopeComponentRegistry',
                     'copy = gaphor.services.copyservice:CopyService',
                     'diagram_export_manager = '
                     'gaphor.services.diagramexportmanager:DiagramExportManager',
                     'diagram_layout = '
                     'gaphor.plugins.diagramlayout:DiagramLayout',
                     'element_dispatcher = '
                     'gaphor.services.elementdispatcher:ElementDispatcher',
                     'element_factory = '
                     'gaphor.UML.elementfactory:ElementFactoryService',
                     'file_manager = gaphor.services.filemanager:FileManager',
                     'help = gaphor.services.helpservice:HelpService',
                     'main_window = gaphor.ui.mainwindow:MainWindow',
                     'properties = gaphor.services.properties:Properties',
                     'pynsource = gaphor.plugins.pynsource:PyNSource',
                     'sanitizer = '
                     'gaphor.services.sanitizerservice:SanitizerService',
                     'undo_manager = gaphor.services.undomanager:UndoManager',
                     'xmi_export = gaphor.plugins.xmiexport:XMIExport'],
 'gaphor.uicomponents': ['consolewindow = '
                         'gaphor.ui.consolewindow:ConsoleWindow',
                         'diagrams = gaphor.ui.mainwindow:Diagrams',
                         'elementeditor = '
                         'gaphor.ui.elementeditor:ElementEditor',
                         'namespace = gaphor.ui.mainwindow:Namespace',
                         'toolbox = gaphor.ui.mainwindow:Toolbox']}

setup_kwargs = {
    'name': 'gaphor',
    'version': '1.0.1',
    'description': 'Gaphor is the simple modeling tool written in Python.',
    'long_description': '# Gaphor <img src="iconsrc/gaphor.svg" width="48">\n\n[![Build Status](https://dev.azure.com/gaphor-dev/gaphor/_apis/build/status/gaphor.gaphor?branchName=master)](https://dev.azure.com/gaphor-dev/gaphor/_build/latest?definitionId=2&branchName=master)\n![Docs build state](https://readthedocs.org/projects/gaphor/badge/?version=latest)\n[![Coverage Status](https://coveralls.io/repos/github/gaphor/gaphor/badge.svg?branch=master)](https://coveralls.io/github/gaphor/gaphor?branch=master)\n[![PyPI](https://img.shields.io/pypi/v/gaphor.svg)](https://pypi.org/project/gaphor)\n[![Downloads](https://pepy.tech/badge/gaphor)](https://pepy.tech/project/gaphor)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat)](https://github.com/RichardLitt/standard-readme)\n[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/Gaphor/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n[![All Contributors](https://img.shields.io/badge/all_contributors-20-orange.svg?style=flat-square)](#contributors)\n\n\n> Gaphor is the simple modeling tool for UML.\n\n![Gaphor Demo](docs/images/gaphor-demo.gif)\n\nGaphor is a simple and easy to use modeling tool for UML. It is aimed at\nbeginning modelers who want a simple and fast tool so that they can focus on\nlearning modeling of software and systems. It is not a full featured enterprise\ntool.\n\n## :bookmark_tabs: Table of Contents\n\n- [Background](#background)\n- [Install](#install)\n- [Usage](#usage)\n- [Contributing](#contributing)\n- [License](#license)\n\n## :scroll: Background\n\nGaphor is a UML modeling application written in Python. It is designed to be\neasy to use, while still being powerful. Gaphor implements a fully-compliant UML\n2 data model, so it is much more than a picture drawing tool. You can use Gaphor\nto quickly visualize different aspects of a system as well as create complete,\nhighly complex models.\n\nGaphor is designed around the following principles:\n\n- Simplicity: The application should be easy to use. Only some basic knowledge of UML is required.\n- Consistency: UML is a graphical modeling language, so all modeling is done in a diagram.\n- Workability: The application should not bother the user every time they do something non-UML-ish.\n\nGaphor is built on [Gaphas](https://github.com/gaphor/gaphas), which provides\nthe foundational diagramming library. It is a GUI application that is built on\nGTK and cairo, [PyGObject](https://pygobject.readthedocs.io/) provides access\nto the GUI toolkit, and [PyCairo](https://pycairo.readthedocs.io/) to the 2D\ngraphics library.\n\n## :floppy_disk: Install\n\n### Windows\nTo install Gaphor on Windows you an use the [latest Gaphor.exe installer](https://github.com/gaphor/gaphor/releases).\nThere are two versions:\n1. Full Windows installation\n2. Portable installation\n\n### Linux\nTo install Gaphor in Linux use Flatpak:\n1. [Install Flatpak](https://flatpak.org/setup)\n1. `flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo`\n1. `flatpak install --user flathub org.gaphor.Gaphor`\n\nAlternatively, you can download the [latest\ngaphor-linux.tar.gz](https://github.com/gaphor/gaphor/releases).\n\n### macOS\nWe are still working on packaging GTK with Gaphor and it is currently an\ninstallation pre-requisite.\n1. Install [homebrew](https://brew.sh)\n1. Open a terminal and execute:\n```bash\n$ brew install gobject-introspection gtk+3\nThen install Gaphor on macOS using the [latest gaphor-macOS.dmg\ninstaller](https://github.com/gaphor/gaphor/releases).\nNote: Sometimes launching the app the first time after installation fails due\nto macOS security settings, please attempt to launch it a 2nd time if this\nhappens.\n\n### PyPI\nYou can also install Gaphor using a wheel from PyPI.\n\nOn Ubuntu 18.04, make sure the following packages are installed:\n\n* libcairo2-dev\n* libgirepository1.0-dev\n* gobject-introspection (a dependency of libgirepository1.0-dev)\n\nGTK+ 3.x is installed by default.\n\n```bash\n$ pip install gaphor\n$ gaphor\n```\nUse of a\n[virtual environment](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments)\nis highly recommended.\n\n### Development\n\n#### Windows\n\nNOTE: Use of virtual environments with msys2 is currently\n[broken](https://github.com/msys2/MINGW-packages/issues/5001).\nTo setup a development environment in Windows:\n1) Go to http://www.msys2.org/ and download the x86_64 installer\n1) Follow the instructions on the page for setting up the basic environment\n1) Run ``C:\\msys64\\mingw64.exe`` - a terminal window should pop up\n```bash\n$ pacman -Suy\n$ pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3-gobject mingw-w64-x86_64-python3-cairo\n$ pacman -S mingw-w64-x86_64-python3-pip mingw-w64-x86_64-python3-setuptools mingw-w64-x86_64-python3-zope.interface\n```\nInstall git if it isn\'t already installed in msys2 with `pacman -S git`\n\ngit clone the repository to C:\\msys64\\home\\<user>\n```bash\n$ cd gaphor\n$ pip3 install -e .\n```\n\n#### Linux\nTo setup a development environment with Linux:\n```bash\n$ sudo apt-get install -y python3-dev python3-gi python3-gi-cairo\n    gir1.2-gtk-3.0 libgirepository1.0-dev libcairo2-dev\n$ source ./venv\n```\n\n#### macOS\nTo setup a development environment with macOS:\n1. Install [homebrew](https://brew.sh)\n1. Open a terminal and execute:\n```bash\n$ brew install gobject-introspection gtk+3\n$ source ./venv\n```\n\n## :flashlight: Usage\n### Creating models\n\nOnce Gaphor is started a new empty model is automatically created. The main\ndiagram is already open in the Diagram section.\n\nSelect an element you want to place, for example a Class, by clicking on the icon in\nthe Toolbox and click on the diagram. This will place a new\nClass item instance on the diagram and add a new Class to the model (it shows\nup in the Navigation). The selected tool will reset itself to\nthe Pointer tool if the option \'\'Diagram -> Reset tool\'\' is selected.\n\nSome elements are not directly visible. The section in the toolbox is collapsed\nand needs to be clicked first to reveal its contents.\n\nGaphor only has one diagram type, and it does not enforce which elements should\nbe placed on a diagram.\n\n### Create a New Diagram\n\n1. Use the Navigation to select an element that can contain a diagram (a\nPackage or Profile)\n1. Select Diagram, and New diagram. A new diagram is created.\n\n### Copy and Paste\n\nItems in a diagram can be copied and pasted in the same diagram or other\ndiagrams. Pasting places an existing item in the diagram, but the item itself\nis not duplicated. In other words, if you paste a Class object in a diagram,\nthe Class will be added to the diagram, but there will be no new Class in the\nNavigation.\n\n### Drag and Drop\n\nAdding an existing element to a diagram is done by dragging the element from\nthe Navigation section onto a diagram. Diagrams and attribute/operations of a\nClass show up in the Navigation but can not be added to a diagram.\n\nElements can also be dragged within the Navigation in order to rearrange them\nin to different packages.\n\n\n## :heart: Contributing\n\nThanks goes to these wonderful people ([emoji key](https://github.com/kentcdodds/all-contributors#emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore -->\n| [<img src="https://avatars0.githubusercontent.com/u/96249?v=4" width="100px;" alt="Arjan Molenaar"/><br /><sub><b>Arjan Molenaar</b></sub>](https://github.com/amolenaar)<br />[💻](https://github.com/danyeaw/gaphor/commits?author=amolenaar "Code") [🐛](https://github.com/danyeaw/gaphor/issues?q=author%3Aamolenaar "Bug reports") [📖](https://github.com/danyeaw/gaphor/commits?author=amolenaar "Documentation") [👀](#review-amolenaar "Reviewed Pull Requests") [💬](#question-amolenaar "Answering Questions") [🐛](https://github.com/danyeaw/gaphor/issues?q=author%3Aamolenaar "Bug reports") [🔌](#plugin-amolenaar "Plugin/utility libraries") [⚠️](https://github.com/danyeaw/gaphor/commits?author=amolenaar "Tests") | [<img src="https://avatars2.githubusercontent.com/u/105664?v=4" width="100px;" alt="wrobell"/><br /><sub><b>wrobell</b></sub>](https://github.com/wrobell)<br />[💻](https://github.com/danyeaw/gaphor/commits?author=wrobell "Code") [⚠️](https://github.com/danyeaw/gaphor/commits?author=wrobell "Tests") [🐛](https://github.com/danyeaw/gaphor/issues?q=author%3Awrobell "Bug reports") [🎨](#design-wrobell "Design") | [<img src="https://avatars1.githubusercontent.com/u/10014976?v=4" width="100px;" alt="Dan Yeaw"/><br /><sub><b>Dan Yeaw</b></sub>](https://ghuser.io/danyeaw)<br />[💻](https://github.com/danyeaw/gaphor/commits?author=danyeaw "Code") [⚠️](https://github.com/danyeaw/gaphor/commits?author=danyeaw "Tests") [📖](https://github.com/danyeaw/gaphor/commits?author=danyeaw "Documentation") [📦](#platform-danyeaw "Packaging/porting to new platform") [🚇](#infra-danyeaw "Infrastructure (Hosting, Build-Tools, etc)") [🐛](https://github.com/danyeaw/gaphor/issues?q=author%3Adanyeaw "Bug reports") [💬](#question-danyeaw "Answering Questions") | [<img src="https://avatars2.githubusercontent.com/u/33630433?v=4" width="100px;" alt="melisdogan"/><br /><sub><b>melisdogan</b></sub>](https://github.com/melisdogan)<br />[📖](https://github.com/danyeaw/gaphor/commits?author=melisdogan "Documentation") | [<img src="https://avatars2.githubusercontent.com/u/114619?v=4" width="100px;" alt="Adam Boduch"/><br /><sub><b>Adam Boduch</b></sub>](http://www.boduch.ca)<br />[💻](https://github.com/danyeaw/gaphor/commits?author=adamboduch "Code") [⚠️](https://github.com/danyeaw/gaphor/commits?author=adamboduch "Tests") [🐛](https://github.com/danyeaw/gaphor/issues?q=author%3Aadamboduch "Bug reports") | [<img src="https://avatars3.githubusercontent.com/u/535113?v=4" width="100px;" alt="Enno Gröper"/><br /><sub><b>Enno Gröper</b></sub>](https://github.com/egroeper)<br />[💻](https://github.com/danyeaw/gaphor/commits?author=egroeper "Code") | [<img src="https://avatars2.githubusercontent.com/u/23027708?v=4" width="100px;" alt="JensPfeifle"/><br /><sub><b>JensPfeifle</b></sub>](https://pfeifle.tech)<br />[📖](https://github.com/danyeaw/gaphor/commits?author=JensPfeifle "Documentation") |\n| :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n| [<img src="https://avatars1.githubusercontent.com/u/927233?v=4" width="100px;" alt="Alexis Howells"/><br /><sub><b>Alexis Howells</b></sub>](http://www.aejh.co.uk)<br />[📖](https://github.com/danyeaw/gaphor/commits?author=aejh "Documentation") | [<img src="https://avatars1.githubusercontent.com/u/124361?v=4" width="100px;" alt="Encolpe DEGOUTE"/><br /><sub><b>Encolpe DEGOUTE</b></sub>](http://encolpe.wordpress.com)<br />[🌍](#translation-encolpe "Translation") | [<img src="https://avatars1.githubusercontent.com/u/309979?v=4" width="100px;" alt="Christian Hoff"/><br /><sub><b>Christian Hoff</b></sub>](https://github.com/choff)<br />[💻](https://github.com/danyeaw/gaphor/commits?author=choff "Code") | [<img src="https://avatars3.githubusercontent.com/u/929712?v=4" width="100px;" alt="Jordi Mallach"/><br /><sub><b>Jordi Mallach</b></sub>](https://oskuro.net/)<br />[🌍](#translation-jmallach "Translation") | [<img src="https://avatars3.githubusercontent.com/u/43508092?v=4" width="100px;" alt="Tony"/><br /><sub><b>Tony</b></sub>](https://github.com/tonytheleg)<br />[🚧](#maintenance-tonytheleg "Maintenance") | [<img src="https://avatars0.githubusercontent.com/u/3011242?v=4" width="100px;" alt="Jan"/><br /><sub><b>Jan</b></sub>](https://github.com/jischebeck)<br />[🐛](https://github.com/danyeaw/gaphor/issues?q=author%3Ajischebeck "Bug reports") | [<img src="https://avatars2.githubusercontent.com/u/203343?v=4" width="100px;" alt="Brock Tibert"/><br /><sub><b>Brock Tibert</b></sub>](http://btibert3.github.io)<br />[🐛](https://github.com/danyeaw/gaphor/issues?q=author%3ABtibert3 "Bug reports") |\n| [<img src="https://avatars2.githubusercontent.com/u/23944?v=4" width="100px;" alt="Rafael Muñoz Cárdenas"/><br /><sub><b>Rafael Muñoz Cárdenas</b></sub>](http://www.rmunoz.net)<br />[🐛](https://github.com/danyeaw/gaphor/issues?q=author%3AMenda "Bug reports") | [<img src="https://avatars2.githubusercontent.com/u/172974?v=4" width="100px;" alt="Mikhail Bessonov"/><br /><sub><b>Mikhail Bessonov</b></sub>](https://github.com/mbessonov)<br />[🐛](https://github.com/danyeaw/gaphor/issues?q=author%3Ambessonov "Bug reports") | [<img src="https://avatars3.githubusercontent.com/u/21650?v=4" width="100px;" alt="Kapil Thangavelu"/><br /><sub><b>Kapil Thangavelu</b></sub>](http://twitter.com/kapilvt)<br />[🐛](https://github.com/danyeaw/gaphor/issues?q=author%3Akapilt "Bug reports") | [<img src="https://avatars2.githubusercontent.com/u/25516?v=4" width="100px;" alt="DimShadoWWW"/><br /><sub><b>DimShadoWWW</b></sub>](https://github.com/DimShadoWWW)<br />[🐛](https://github.com/danyeaw/gaphor/issues?q=author%3ADimShadoWWW "Bug reports") | [<img src="https://avatars2.githubusercontent.com/u/96399?v=4" width="100px;" alt="Nedko Arnaudov"/><br /><sub><b>Nedko Arnaudov</b></sub>](http://nedko.arnaudov.name)<br />[🐛](https://github.com/danyeaw/gaphor/issues?q=author%3Anedko "Bug reports") | [<img src="https://avatars2.githubusercontent.com/u/3226457?v=4" width="100px;" alt="Alexander Wilms"/><br /><sub><b>Alexander Wilms</b></sub>](https://github.com/Alexander-Wilms)<br />[🐛](https://github.com/danyeaw/gaphor/issues?q=author%3AAlexander-Wilms "Bug reports") |\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the\n[all-contributors](https://github.com/kentcdodds/all-contributors)\nspecification. Contributions of any kind are welcome!\n\n1.  Check for open issues or open a fresh issue to start a discussion\n    around a feature idea or a bug. There is a\n    [first-timers-only](https://github.com/gaphor/gaphor/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3Afirst-timers-only)\n    tag for issues that should be ideal for people who are not very\n    familiar with the codebase yet.\n2.  Fork [the repository](https://github.com/gaphor/gaphor) on\n    GitHub to start making your changes to the **master** branch (or\n    branch off of it).\n3.  Write a test which shows that the bug was fixed or that the feature\n    works as expected.\n4.  Send a pull request and bug the maintainers until it gets merged and\n    published. :smile:\n\nSee [the contributing file](CONTRIBUTING.md)!\n\n\n## :copyright: License\nCopyright (C) Arjan Molenaar and Dan Yeaw\n\nLicensed under the [Apache License v2](LICENSE.txt).\n\nSummary: You can do what you like with Gaphor, as long as you include the\nrequired notices. This permissive license contains a patent license from the\ncontributors of the code.\n',
    'author': 'Arjan J. Molenaar',
    'author_email': 'gaphor@gmail.com',
    'url': 'https://gaphor.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
