Name:           waffle
Version:        1.2.2
Release:        1
Summary:        Cross-platform C library for runtime selection of GL API and window system
Source0:        %{name}-%{version}.tar.gz
Patch0:         0001-Require-wayland-egl-version-9.0.patch
Group:          Development/Libraries
License:        BSD
URL:            http://people.freedesktop.org/~chadversary/waffle

BuildRequires:  cmake
BuildRequires:  wayland-devel
BuildRequires:  mesa-llvmpipe-libGL-devel
BuildRequires:  mesa-llvmpipe-libGLESv1-devel
BuildRequires:  mesa-llvmpipe-libGLESv2-devel
BuildRequires:  mesa-llvmpipe-libEGL-devel
BuildRequires:  mesa-llvmpipe-libwayland-egl-devel

%description
Waffle is a cross-platform C library that allows one to defer selection of GL 
API and window system until runtime. For example, on Linux, Waffle enables an 
application to select X11/EGL with an OpenGL 3.3 core profile, Wayland with 
OpenGL ES2, and other window system / API combinations.


%package devel
Summary: Waffle header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files for waffle. Install this package if you 
want to write or compile a program that needs waffle.

%prep
%setup -q
%patch0 -p1

%build
cd waffle
cmake -DCMAKE_INSTALL_PREFIX=/usr \
      -Dwaffle_has_glx=ON \
      -Dwaffle_has_wayland=ON \
      -Dwaffle_has_x11_egl=ON \
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
/usr/share/doc/waffle-1/*
/usr/share/cmake/Modules/*
%{_libdir}/libwaffle-1.so
%{_libdir}/pkgconfig/*

