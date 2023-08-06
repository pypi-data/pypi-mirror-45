import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloudflarekv",
    version="0.0.0",
    author="AppointmentGuru",
    author_email="tech@appointmentguru.co",
    description="Super simple access to cloudflare workers kv store",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/toast38coza/cloudflarekv",
    packages=['.'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
