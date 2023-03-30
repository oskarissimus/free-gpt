from mercury.utils import omit_lines


def test_omit_lines():
    input = """Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease
Get:2 http://security.ubuntu.com/ubuntu jammy-security InRelease [110 kB]                                                     
Get:3 https://apt.releases.hashicorp.com jammy InRelease [12.9 kB]                                                                       
Get:4 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [119 kB]                                                                               
Get:5 https://packages.cloud.google.com/apt cloud-sdk InRelease [6361 B]                                           
Get:6 https://apt.releases.hashicorp.com jammy/main amd64 Packages [81.1 kB]                         
Get:7 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [107 kB]
Get:8 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [728 kB]
Get:9 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [986 kB]
Get:10 http://security.ubuntu.com/ubuntu jammy-security/main Translation-en [146 kB]
Get:11 http://security.ubuntu.com/ubuntu jammy-security/main amd64 c-n-f Metadata [9016 B]    
Get:12 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [701 kB]
Get:13 http://security.ubuntu.com/ubuntu jammy-security/restricted Translation-en [109 kB]      
Get:14 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [715 kB]
Get:15 http://archive.ubuntu.com/ubuntu jammy-updates/main Translation-en [210 kB]
Get:16 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 c-n-f Metadata [14.1 kB]
Get:17 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 c-n-f Metadata [13.9 kB]
Get:18 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [739 kB]
Get:19 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [898 kB]
Get:20 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 c-n-f Metadata [18.5 kB]
Get:21 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [20.3 kB]
Get:22 http://archive.ubuntu.com/ubuntu jammy-backports/universe Translation-en [14.4 kB]
Get:23 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 c-n-f Metadata [480 B]
Fetched 5759 kB in 1s (4861 kB/s)                                     
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
All packages are up to date."""
    expected = """Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease
Get:2 http://security.ubuntu.com/ubuntu jammy-security InRelease [110 kB]                                                     
Get:3 https://apt.releases.hashicorp.com jammy InRelease [12.9 kB]                                                                       
Get:4 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [119 kB]                                                                               
Get:5 https://packages.cloud.google.com/apt cloud-sdk InRelease [6361 B]                                           
(*** 18 lines omitted ***)
Fetched 5759 kB in 1s (4861 kB/s)                                     
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
All packages are up to date."""

    assert omit_lines(input) == expected