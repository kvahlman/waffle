Name:           libhybris-waffle
Version:        1.3.0
Release:        1
Summary:        Cross-platform C library for runtime selection of GL API and window system
Source0:        %{name}-%{version}.tar.gz
Patch0:         0001-cmake-Depend-on-libhybris-s-version-of-wayland-egl.patch
Patch1:         0002-egl-Allow-building-against-older-EGL-headers.patch
Patch2:         0003-tests-Install-test-library-and-functional-tests.patch
Patch3:         0004-tests-Disable-GLES-1.1-test-that-brings-the-test-pro.patch

Group:          Development/Libraries
License:        BSD
URL:            http://people.freedesktop.org/~chadversary/waffle

BuildRequires:  cmake
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(wayland-egl) 
Conflicts:      waffle

%description
Waffle is a cross-platform C library that allows one to defer selection of GL 
API and window system until runtime. For example, on Linux, Waffle enables an 
application to select X11/EGL with an OpenGL 3.3 core profile, Wayland with 
OpenGL ES2, and other window system / API combinations.

This package is specifically for libhybris enabled EGL

%package devel
Summary: Waffle header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files for waffle. Install this package if you 
want to write or compile a program that needs waffle.

%package test
Summary: Waffle tests
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description test
This package contains some test programs for waffle.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cd waffle
cmake -DCMAKE_INSTALL_PREFIX=/usr \
      -Dwaffle_has_glx=OFF \
      -Dwaffle_has_wayland=ON \
      -Dwaffle_has_x11_egl=OFF \
      -Dwaffle_has_gbm=OFF
make

%install
cd waffle
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libwaffle-1.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/waffle-1/*
/usr/share/doc/waffle1/*
/usr/share/cmake/Modules/*
%{_libdir}/libwaffle-1.so
%{_libdir}/pkgconfig/*

%files test
%defattr(-,root,root,-)
%{_libdir}/libwaffle_test.so
%{_bindir}/gl_basic_test

