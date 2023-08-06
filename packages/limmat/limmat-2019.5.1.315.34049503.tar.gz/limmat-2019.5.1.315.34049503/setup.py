import datetime
import hashlib
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def version():
    h = hashlib.sha3_256()

    with open("setup.py", "rb") as fh:
        h.update(b"./setup.py")
        h.update(fh.read())

    with open("limmat.py", "rb") as fh:
        h.update(b"./limmat.py")
        h.update(fh.read())

    x = int(h.hexdigest()[:7], 16)

    t = datetime.datetime.utcnow()
    s = datetime.datetime.fromisoformat(t.date().isoformat())
    d = int((t.timestamp() - s.timestamp()) / 86.48)
    return f"{t.year}.{t.month:02d}.{t.day:02d}.{d:03d}.{x}"


setuptools.setup(
    name="limmat",
    version=version(),
    author="Tobias Ammann",
    # author_email="",
    description="I sat by the river and thought about WSGI...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/limmat/",
    # packages=setuptools.find_packages(),
    py_modules=["limmat"],
    platforms="any",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
