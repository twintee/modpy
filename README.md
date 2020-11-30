modpy
# modpy
===============

## usage

### case hard coding

1. clone this repository. and import from relational path.

<pre>
sys.path.append(os.path.join(os.path.dirname(__file__), './modpy'))
</pre>

1. install module
request python module:
<pre>
pip install -r modpy/requirements.txt
</pre>

1. ignore clone path.

### use pth file

1. add pth file in sys.path list site-package. and edit follow code.
<pre>
./modpy
</pre>

1. clone this repository in site-package path include pth file.

## include modules

* helper.py
    1. import package
    <pre>
    import helper as fn
    </pre>

* mm.py
    1. import class
    <pre>
    from mm import MatterMost
    </pre>
