Summary:	KernelShark - front-end reader of tracing data
Summary(pl.UTF-8):	KernelShark - graficzny interfejs do czytania danych ze śledzenia
Name:		kernelshark
Version:	2.2.1
Release:	1
License:	GPL v2
Group:		X11/Development/Tools
#Source0Download: https://git.kernel.org/pub/scm/utils/trace-cmd/kernel-shark.git/
Source0:	https://git.kernel.org/pub/scm/utils/trace-cmd/kernel-shark.git/snapshot/%{name}-v%{version}.tar.gz
# Source0-md5:	a9600979bf2ae5b44e34220b73875f1e
URL:		https://kernelshark.org/
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	Qt5Network-devel >= 5.15
BuildRequires:	Qt5Widgets-devel >= 5.15
BuildRequires:	asciidoc
BuildRequires:	cmake >= 3.1.2
BuildRequires:	doxygen
BuildRequires:	json-c-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libtracecmd-devel >= 1.0
BuildRequires:	libtraceevent-devel
BuildRequires:	libtracefs-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
Requires:	Qt5Network >= 5.15
Requires:	Qt5Widgets >= 5.15
# FreeSans
Requires:	fonts-TTF-freefont
Obsoletes:	trace-cmd-gui < 2.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KernelShark is a front-end reader of tracing data.

%description -l pl.UTF-8
KernelShark to graficzny interfejs do odczytu danych ze śledzenia.

%package devel
Summary:	Header files for libkshark library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libkhark
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	json-c-devel
Requires:	libtracecmd-devel >= 1.0

%description devel
Header files for libkshark library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libkhark.

%prep
%setup -q -n %{name}-v%{version}

# disable find
%{__sed} -i -e 's/^FIND_MANPAGE_DOCBOOK_XSL := /#&/' Documentation/Makefile

%build
install -d builddir
cd builddir
%cmake .. \
	-D_INSTALL_PREFIX=%{_prefix} \
	-D_LIBDIR=%{_libdir} \
	-DTRACECMD_EXECUTABLE=%{_bindir}/trace-cmd \
	-DTT_FONT_FILE=%{_fontsdir}/TTF/FreeSans.ttf

%{__make}
cd ..

%{__make} -C Documentation \
	MANPAGE_DOCBOOK_XSL=%{py3_sitescriptdir}/asciidoc/resources/docbook-xsl/manpage.xsl \
	VERBOSE=1 \
	kshark-dir=$(pwd)

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C Documentation install \
	DESTDIR_SQ=$RPM_BUILD_ROOT \
	INSTALL=install \
	kshark-dir=$(pwd) \
	html_install_SQ=%{_docdir}/%{name} \
	img_install_SQ=%{_docdir}/%{name} \
	man_dir_SQ=%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/kernelshark
%attr(755,root,root) %{_bindir}/kshark-record
%attr(755,root,root) %{_bindir}/kshark-su-record
%attr(755,root,root) %{_libdir}/libkshark.so.%{version}
%attr(755,root,root) %ghost %{_libdir}/libkshark.so.2
%attr(755,root,root) %{_libdir}/libkshark-gui.so.%{version}
%attr(755,root,root) %{_libdir}/libkshark-plot.so.%{version}
%dir %{_libdir}/kernelshark
%dir %{_libdir}/kernelshark/plugins
%attr(755,root,root) %{_libdir}/kernelshark/plugins/plugin-*.so
%{_datadir}/polkit-1/actions/org.freedesktop.kshark-record.policy
%{_desktopdir}/kernelshark.desktop
%{_iconsdir}/kernelshark
%{_mandir}/man1/kernelshark.1*
%{_docdir}/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkshark.so
%{_includedir}/kernelshark
%{_pkgconfigdir}/libkshark.pc
