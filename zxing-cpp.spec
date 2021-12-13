Name: zxing-cpp
Version: 1.2.0
Release: 1%{?dist}
Summary: C++ port of the ZXing ("Zebra Crossing") barcode scanning library

# The entire source is ASL 2.0, except:
#
# - TextCodec files, that is, core/src/textcodec/*, are
#   (LGPLv2 with exceptions or LGPLv3 with exceptions).
#   - core/src/textcodec/JPText{En,De}coder.* are, formally,
#     ((LGPLv2 with exceptions or LGPLv3 with exceptions) and BSD),
#     which still forms an effective license of
#     (LGPLv2 with exceptions or LGPLv3 with exceptions)
# - wrappers/wasm/base64ArrayBuffer.js is MIT (but is not used)
# - thirdparty/stb/stb_image.h and thirdparty/stb/stb_image_write.h are MIT
#   (but are unbundled)
#
# The resulting effective license for the combined library is:
License: LGPLv2 with exceptions or LGPLv3 with exceptions
Url: https://github.com/nu-book/zxing-cpp
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: cmake(fmt)
# -static BR’s required by guidelines for tracking of header-only libraries:
BuildRequires: stb_image-devel
BuildRequires: stb_image-static
BuildRequires: stb_image_write-devel
BuildRequires: stb_image_write-static
# https://github.com/nu-book/zxing-cpp/issues/248
Patch0: 0001-Add-a-mode-to-build-against-system-versions-of-depen.patch
# Update stb_image/stb_image_write
# https://github.com/nu-book/zxing-cpp/pull/269
# Fixes CVE-2021-28021, CVE-2021-42715, and CVE-2021-42716, and adds a patch
# file for zxing-cpp-specific changes
Patch1: %{url}/pull/269.patch

%description
ZXing-C++ ("zebra crossing") is an open-source, multi-format 1D/2D barcode
image processing library implemented in C++.

%package devel
# The entire contents are ASL 2.0, except:
#
#   - %%{_includedir}/ZXing/textcodec/*.h are exactly or effectively 
#     (LGPLv2 with exceptions or LGPLv3 with exceptions)
#
# See licensing breakdown above base package’s License field for further
# details.
License: ASL 2.0 and (LGPLv2 with exceptions or LGPLv3 with exceptions)
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1
# remove bundled stb libraries:
rm -v thirdparty/stb/stb_image_write.h thirdparty/stb/stb_image.h
# stb_image.h is trivially forked: reconstruct the changes with the latest
# unbundled copy
cp -p %{_includedir}/stb/stb_image.h thirdparty/stb/
pushd thirdparty/stb
patch -p1 < stb_image.patch
popd

%build
%cmake -DBUILD_EXAMPLES=OFF
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE LICENSE.ZXing LICENSE.Qt LGPL_EXCEPTION.Qt NOTICE
%{_libdir}/libZXing.so.1
%{_libdir}/libZXing.so.%{version}

%files devel
%doc README.md
%{_includedir}/ZXing/
%{_libdir}/libZXing.so
%{_libdir}/cmake/ZXing/
%{_libdir}/pkgconfig/zxing.pc

%changelog
* Fri Dec 10 2021 Caolán McNamara <caolanm@redhat.com> 1.2.0-1
- initial import
