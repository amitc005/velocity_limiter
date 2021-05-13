from setuptools import setup

setup(
    name="VelocityLimiter",
    version="1.0",
    py_modules=["velocity_limiter"],
    install_requires=["Click"],
    entry_points="""
        [console_scripts]
        velocity_limiter=main:cli
    """,
)
