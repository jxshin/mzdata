#!/opt/exptools/perl/bin/perl
# may be get from line too, in case stacie wants to use it

#use HTML::Parse;
#use HTML::FormatText;


sub fill {
	local ($key,$val)=@_;
	#$val=HTML::FormatText->new->format(parse_html($val));
	$val=~s/\&nbsp\;//g;
	#$val=~s/\=/EQUALS_TO/g;
	$val=~s/\&\#64\;/@/g;
	$val=~s/\<[^\>]*\>//g;
	$val=~s/\;/SEMICOLON/g;	
	$res{$key}=$val;
}

$start0=0;$start1=0;$start2=0;
$nline=0;

sub output {
	@keys=sort keys %res;
	if ($#keys >= 0){
		print "$nline\;";
		print $#keys;		
		foreach $key (@keys){
			print "\;$key=$res{$key}";
		}
		print "\n";
	}
	undef %res;
}
my $who = "";
my $when = "";
while (<STDIN>){
	$nline++;
	chop ();
	if (/^\s*\<\/head\>/){
		#print STDERR "started head\n";
		$start0=1;$start1=0;$start2=0;
	}
	if (/^(HTTP\/1\.1 200 OK|\<html\>)$/){
		$start0=0;$start1=0;$start2=0;
		output();
	}
	if ($start0==1 && /Activity log for bug (\d+):/){
		#print STDERR "started0\n";
		$start0=0;$start1=1;$start2=0;
		&fill ("Bug", $1);
	}
	if ($start1==1 && /\Q<th>Who<\/th>\E/){
		#print STDERR "started1\n";
		while ($_ !~ /\<\/tr\>/) {
			$_ = <STDIN>;
			$nline++;
		}
		$start0=0;$start1=0;$start2=1;
		$changes=-1;
		next;
	}
	if ($start2==1){
		#got to read entire table :-(
		chop();
		$line = $_;
		while ($_ !~ /\<\/table\>/) {
			$_ = <STDIN>;
			$nline++;
			chop();
			$line .= $_;
		}
		$start2=0;
		$line =~ s/[\n\r]//g;
		$line =~ s/\<\/tr\>\s*\<tr/\<\/tr\>\n\<tr/g;
		$changes = -1;
		for my $l (split(/\n/, $line, -1)){
			$changes ++;
			$variable=-1;
			$l =~ s/\<\/td\>\s*\<td/\<\/td\>\n\<td/g;
			my @l0s = split(/\n/, $l, -1);
			$variable = 3-$#l0s; #to make sure we get the right column
			if ($variable >= 0 && $who ne ""){
				&fill ("$changes:0", $who);
			}
			if ($variable >= 1 && $when ne ""){
				&fill ("$changes:1", $when);
			}
			for my $l0 (@l0s){
				if ($l0 =~ /\<td[^\>]*\>\s*(.*)\s*\<\/td\>/) {
					my $val = $1; $val =~ s/\s*$//;
					$variable++;
					$who = $val if $variable == 0;
					$when = $val if $variable == 1;
					#print STDERR "$changes:$variable=$val\n";
					&fill ("$changes:$variable", $val);
				}
			}
		}
		$who = "";
		$when = "";
	}
}
output();




