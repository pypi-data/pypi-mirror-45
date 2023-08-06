import setuptools

setuptools.setup(
    name="jupyter-syncthing-proxy",
    version='1.0dev2',
    url="https://github.com/jupyterhub/jupyter-server-proxy/tree/master/contrib/syncthing",
    author="Project Jupyter Contributors",
    description="projectjupyter@gmail.com",
    packages=setuptools.find_packages(),
	keywords=['Jupyter'],
	classifiers=['Framework :: Jupyter'],
    install_requires=[
        'jupyter-server-proxy>=1.0.1'
    ],
    entry_points={
        'jupyter_serverproxy_servers': [
            'syncthing = jupyter_syncthing_proxy:setup_syncthing',
        ]
    },
    package_data={
        'jupyter_syncthing_proxy': ['icons/*'],
    },
)
