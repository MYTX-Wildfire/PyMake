FROM ubuntu:jammy
USER root

ARG USERNAME
ARG USER_UID
ARG USER_GID
ARG PYTHON_VERSION=3.11

# Install apt packages
RUN apt-get update -y && \
	apt-get install -y \
		git \
		ninja-build \
		python${PYTHON_VERSION} \
		python3-pip \
		ssh \
		sudo \
		vim && \
	update-alternatives --install \
		/usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 3

# Install pip packages
RUN python3 -m pip install \
	# Primary mkdocs package
	mkdocs \
	# Packages used to enable the material mkdocs theme
	mkdocs-material \
	mkdocs-git-revision-date-localized-plugin \
	pygments \
	# Packages for enabling plantuml support
	plantuml-markdown \
	# Other
	autopep8 \
	coverage \
	pytest \
	pytest-cov

# Add CMake 3.14
RUN mkdir -p /tmp/${USERNAME} && \
	wget -O /tmp/${USERNAME}/cmake.tar.gz https://github.com/Kitware/CMake/releases/download/v3.14.5/cmake-3.14.5-linux-x86_64.tar.gz && \
	# Extract the files from the tarball to a temporary directory
	# This is done because the resulting directory structure after extracting
	#   the tarball will look like `/tmp/mythix/cmake/cmake-3.21.3-linux-etc/...`
	mkdir -p /tmp/${USERNAME}/cmake && \
	tar -xvf /tmp/${USERNAME}/cmake.tar.gz -C /tmp/${USERNAME}/cmake && \
	# Move the CMake files into the Tools folder
	mkdir -p /tools/cmake && \
	# Note that 3.14 used "Linux" instead of "linux" in the archive filename
	mv /tmp/${USERNAME}/cmake/cmake-3.14.5-Linux-x86_64 /tools/cmake/3.14.5 && \
	ln -s /tools/cmake/3.14.5/bin/cmake /usr/bin/cmake3.14 && \
	ln -s /tools/cmake/3.14.5/bin/cpack /usr/bin/cpack3.14 && \
	ln -s /tools/cmake/3.14.5/bin/ctest /usr/bin/ctest3.14 && \
	# Remove unnecessary files to keep container image size down
	rm -r /tools/cmake/3.14.5/doc && \
	rm -r /tools/cmake/3.14.5/man && \
	# Make CMake binaries available on the PATH
	update-alternatives --install \
		/usr/bin/cmake cmake /tools/cmake/3.14.5/bin/cmake 314 \
		--slave /usr/bin/cpack cpack /tools/cmake/3.14.5/bin/cpack \
		--slave /usr/bin/ctest ctest /tools/cmake/3.14.5/bin/ctest && \
	# Clean up temporary files
	rm -rf /tmp/${USERNAME}

# Add CMake 3.25
RUN mkdir -p /tmp/${USERNAME} && \
	wget -O /tmp/${USERNAME}/cmake.tar.gz https://github.com/Kitware/CMake/releases/download/v3.25.2/cmake-3.25.2-linux-x86_64.tar.gz && \
	# Extract the files from the tarball to a temporary directory
	# This is done because the resulting directory structure after extracting
	#   the tarball will look like `/tmp/mythix/cmake/cmake-3.21.3-linux-etc/...`
	mkdir -p /tmp/${USERNAME}/cmake && \
	tar -xvf /tmp/${USERNAME}/cmake.tar.gz -C /tmp/${USERNAME}/cmake && \
	# Move the CMake files into the Tools folder
	mkdir -p /tools/cmake && \
	mv /tmp/${USERNAME}/cmake/cmake-3.25.2-linux-x86_64 /tools/cmake/3.25.2 && \
	ln -s /tools/cmake/3.25.2/bin/cmake /usr/bin/cmake3.25 && \
	ln -s /tools/cmake/3.25.2/bin/cpack /usr/bin/cpack3.25 && \
	ln -s /tools/cmake/3.25.2/bin/ctest /usr/bin/ctest3.25 && \
	# Remove unnecessary files to keep container image size down
	rm -r /tools/cmake/3.25.2/doc && \
	rm -r /tools/cmake/3.25.2/man && \
	# Make CMake binaries available on the PATH
	update-alternatives --install \
		/usr/bin/cmake cmake /tools/cmake/3.25.2/bin/cmake 325 \
		--slave /usr/bin/cpack cpack /tools/cmake/3.25.2/bin/cpack \
		--slave /usr/bin/ctest ctest /tools/cmake/3.25.2/bin/ctest && \
	# Clean up temporary files
	rm -rf /tmp/${USERNAME}

# Create the user
RUN groupadd --gid $USER_GID $USERNAME && \
	useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash && \
	echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
	chmod 0440 /etc/sudoers.d/$USERNAME
USER $USERNAME
