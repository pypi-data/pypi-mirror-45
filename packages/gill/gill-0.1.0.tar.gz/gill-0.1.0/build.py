from Cython.Build import cythonize


modules = ['gill/_gill.pyx']
extensions = cythonize(modules, compiler_directives={
    'language_level': '3',
})


def build(setup_kwargs):
    setup_kwargs.update({
        'ext_modules': extensions,
    })
