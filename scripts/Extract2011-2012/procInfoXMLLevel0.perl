#!/opt/exptools/perl/bin/perl
use strict;
use warnings;

require "timelocal.pl";
use Date::Manip qw (ParseDate UnixDate);

my $start0=0;
my $start1=0;
my $start2=0;
my $start3=0;
my $nline=0;
my @keysold=();
my %res;
sub fill {
	my ($key,$val)=@_;
	$key =~ s/[\n\r]/NEWLINE/g;
	$key =~ s/[\;]/SEMICOLON/g;
	$key =~ s/\=/EQUAL/g;
	$val =~ s/[\n\r]/NEWLINE/g;
	$val =~ s/[\;]/SEMICOLON/g;
	$val =~ s/\=/EQUAL/g;
	$res{$key}=$val;
	#print STDERR "$key\;$val\n";
}

sub output {
		my @keys=sort keys %res;
		if ($#keys > 0){
			print "$nline";
			foreach my $key (@keys){
				print "\;$key=$res{$key}";
			}
			@keysold=@keys;
			print "\n";
		}else{
			#print STDERR "$nline\;$#keys\;@keys\n";
		}
		%res = ();
}
while (<STDIN>){
	$nline++;
	chop ();
	if (/^\<bugzilla/){ $start0=1;$start1=0;$start2=0;$start3=0;}
	if (/^\<\/bugzilla\>/){
		$start0=0;$start1=0;$start2=0;$start3=0;
		output();
	}
	if ($start0==1 && /^\s*\<bug\>/){
		$start0=0;$start1=1;$start2=0;$start3=0;
		#print STDERR "in 1\n";
	}
	if (/\<long_desc[^\>]*\>/){
		$start1 = 0;
		$start2 ++;
	}
	if (/^\s*\<attachment/){
		$start1 = 0;
		$start3 ++;
	}
	if ($start1==1) {
		if (/\<bug_id\>(\d*)\<\/bug_id\>/){
			&fill ('Bug#', $1);
			next;
		}
		for my $i ("creation_ts", "delta_ts"){ 
			if (/\<$i\>([^\<]*)\<\/$i\>/){
				#print STDERR "$1\n";
				my $d1=ParseDate($1);
				if ($d1 ne ""){
					my @xx=UnixDate($d1, "%S","%M","%H", "%d", "%m", "%y");
					$xx[4] = substr($d1,4,2);
					$xx[4] --;			 
					my $d2 = &timelocal(@xx);
					&fill($i, $d2);
				}
				next;
			}
		}

# attach

		for my $i ("reporter_accessible", "cclist_accessible", "short_desc", "classification_id", "classification", "product", "component", "version", "rep_platform", "op_sys", "bug_status", "resolution", "", "priority", "bug_severity", "target_milestone", "dependson", "everconfirmed", "reporter", "qa_contact", "assigned_to"){
			if (/\<$i\>([^\<]*)\<\/$i\>/){
				&fill($i, $1);
				next;
			}
		}
		if (/\<cc\>([^\<]*)\<\/cc\>/){
			my $tmp = $1;
			$tmp = "$res{cc}:$tmp" if defined $res{cc};
			&fill("cc", $tmp);
			next;
		}
		for my $i ("assigned_to", "reporter", "qa_contact"){
			if (/\<$i name=\"([^\"]*)\"\>([^\<]*)\<\/$i\>/){
				&fill("$i", $2);
				&fill("${i}_name", $1);
				next;
			}
		}			
	}
	if ($start2) {
		for my $i ("commentid","who","bug_when"){#,"thetext"
			if (/\<$i\>([^\<]*)\<\/$i\>/){
				&fill("long:$start2:$i", $1);
				next;
			}			
		}
		if (/\<who\s*name=\"([^\"]*)\"\>([^\<]*)\<\/who\>/){
			&fill("long:$start2:who", $2);
			&fill("long:$start2:who_name", $1);
			next;		
		}
		my $text = "";
		if (s/\s*\<thetext\>//){
			while ($_ !~ /<\/thetext\>/){
				$text .= $_;
				$_ = <STDIN>;
				$nline++;
				#chop ();
				if (/^\<\/bugzilla\>/){
					$start0=0;$start1=0;$start2=0;$start3=0;
					output();
					die "got in bad state here ---------------\n$text\n----------------:$_:$.:$nline:".($res{"Bug#"})."\n";
				}
			}
			$_ =~ s/<\/thetext\>\s*//;
			$text .= $_;
			#$text =~ s/\r//g;
			#$text =~ s/\n/NEWLINE/g;
			&fill("long:$start2:text", $text);
		}
	}
	if ($start3) {
		for my $i ("attachid","date","attacher","type","size","desc"){#,"thetext
			if (/\<$i\>([^\<]*)\<\/$i\>/){
				&fill("attach:$start3:$i", $1);
				next;
			}
		}			
	}
}
output();



