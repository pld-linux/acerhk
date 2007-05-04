#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
#
%define _rel		3
%define _orig_name	acerhk

Summary:	Linux driver for Acer notebook special Hot Keys
Summary(pl.UTF-8):	Sterownik dla Linuksa obsługujący specjalne klawisze w notebookach Acer
Name:		kernel-misc-%{_orig_name}
Version:	0.5.35
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://www.cakey.de/acerhk/archives/%{_orig_name}-%{version}.tar.bz2
# Source0-md5:	551285657c8ba338f23595af257d21df
URL:		http://www.cakey.de/acerhk/
BuildRequires:	%{kgcc_package}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	modules	acerhk

%description
This is a Linux driver for Acer notebook special Hot Keys.

%description -l pl.UTF-8
Sterownik dla Linuksa pozwalający uaktywnić specjalne przyciski w
notebookach Acer.

%prep
%setup -q -n %{_orig_name}-%{version}

%build
%build_kernel_modules -m %{modules}

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m %{modules} -d misc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-misc-%{_orig_name}
%depmod %{_kernel_ver}

%postun	-n kernel-misc-%{_orig_name}
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc NEWS INSTALL README doc/*
/lib/modules/%{_kernel_ver}/misc/*.ko*
