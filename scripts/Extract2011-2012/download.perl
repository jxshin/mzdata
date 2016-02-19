#!/usr/bin/perl
use strict;
use warnings;
use LWP::Simple;
use LWP::UserAgent;
use LWP::ConnCache;
use HTTP::Cookies;
use Sys::SigAction qw (timeout_call);
use Config::IniFiles;

my $conf = new Config::IniFiles -file=>$ARGV[0];
my $url_pattern = $conf->val("download", "URL_PATTERN");
my $cookie_file = $conf->val("download", "COOKIE_FILE");
my $need_login = $conf->val("download", "NEED_LOGIN");
my $login_url = $conf->val("download", "LOGIN_URL");

my $ua=new LWP::UserAgent;
$ua->agent('Mozilla/5.0');
$ua->cookie_jar(HTTP::Cookies->new(file => $cookie_file, autosave => 1));
$ua->timeout(1200);
$ua->conn_cache(new LWP::ConnCache);

my $res="";
my $req;
if ( $need_login != 0 ){
	$req = new HTTP::Request GET => $login_url;
	$res = $ua ->request ($req);
	if ($res->is_success){
		#print "". ($res ->as_string ()) ."\n";
	}else{
		print STDERR "Could not login. $res\n";
		exit();
	}
}

while (<STDIN>){
	chomp();
	my $id=$_;
	my $url = $url_pattern;
	$url =~ s/\$ID/$id/g;
	$res = undef;
	$req = new HTTP::Request GET => $url;
	if (timeout_call(1800, sub{$res = $ua ->request ($req)})){
		print STDERR "bad $id\n";
	}
	elsif ($res->is_success){
		print $res ->as_string () ."\n";
		print STDERR "$id\n";
	}else{
		print STDERR "bad $id\n";
	}
	sleep(3);
}
