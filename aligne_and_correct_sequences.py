#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from subprocess import call
from pyfasta.fasta import Fasta # Depends on fasta.py from https://github.com/brentp/pyfasta

def create_aligned_file(filename, gapopen=10, gapextend=0.5):
    try:
        f = Fasta(filename)
    except:
        print "Error: '",filename, "' is not a valid file to open!"
        sys.exit(2)
        return
   
    try:
        print "Loded data from file: ", filename
        name_f_sequence = f.items()[0][0];
        print "name_f_sequence = ", name_f_sequence
        name_r_sequence = f.items()[1][0];
        print "name_r_sequence = ", name_r_sequence
    except:
        print "Error: '",filename, "' is not a valid file to Process. "
        print "Skip this file."
        return
    


    print "Finding the reverse complement", name_r_sequence
    command = "revseq " + filename + ":" + name_r_sequence + " " + name_r_sequence + ".fasta"
    
    print ">This command is executed:\n\t",command
    call(command, shell=True)    
    
    
    print "Alligne sequence ",name_f_sequence, "and ", name_r_sequence + ".fasta" 
    
    command = "needle " + filename + ":" + name_f_sequence + " " +name_r_sequence + ".fasta "+ filename + ".needle"
    command = command + " -aformat fasta"    
    command = command + " -gapopen %0.2f"%gapopen # Gap opening penalty [10.0]: 
    command = command + " -gapextend %0.2f "%gapextend # Gap extension penalty [0.5]: 
    
    print ">This command is executed:\n\t",command
    if not call(command, shell=True):
        print "Aligned file was saved to ", filename+".needle"
        return filename+".needle"
    else:
        print "Allignement failed :("
    
    
# ============================ correct_aligned_sequneces.py ===================

def select_from_rule(forw, rev):
    forw_is_good = False
    rev_is_good = False

    # if both are not good then check if forw is a blank
    # if the forward is a blank then it's better to use the reverse
    # even when it is ambigious
    if(forw == '-'):
        return rev

    if(rev == '-'):
	return forw



    # Return the forward if both are similar
    if (forw == rev):
        return forw
        
    # Check the forward base if it is good    
    if (forw == 'T' or forw=='G' or forw=='A' or forw=='C'):
        forw_is_good = True
	#print "forw_is_good"
    else: 
        forw_is_good = False
    # Check the reverse base if it is good    
    if (rev == 'T' or rev=='G' or rev=='A' or rev=='C'):
        rev_is_good = True
	#print "ref__is_good"

    else:
        rev_is_good = False
        
    #print "ref_is_good: ", rev_is_good
    #print "forw_is_good: ", forw_is_good

    if ( forw_is_good and not rev_is_good):
	return forw

    if (not forw_is_good and  rev_is_good):
	return rev

    if (not forw_is_good and not rev_is_good):
        return '?'

    return forw

def run_sequence_correction(filename):
    try:
        f = Fasta(filename)
    except:
        print "Error: '",filename, "' is not a valid file to open!"        
        return
    
    try:
        print "Loded data from file: ", filename
        name_f_sequence = f.items()[0][0];
        print "name_f_sequence = ", name_f_sequence
        name_r_sequence = f.items()[1][0];
        print "name_r_sequence = ", name_r_sequence
    except:
        print "Error: '",filename, "' is not a valid file to Process. "
        print "Skip this file."
        return    
    
    f_sequence = f.get(name_f_sequence)
    r_sequence = f.get(name_r_sequence)
    
    
    new_file_string = ">"+name_f_sequence+"_merged\n"
    
    print " "
    # print "idx\tforw\trev\tmerged"    # only for debug
    for base_idx in range(len(f_sequence)):
        forw = f_sequence[base_idx]
        rev =  r_sequence[base_idx]
        # Select the merged base from the rules above
        merged = select_from_rule(forw, rev)
        #print base_idx+1, "\t", forw,  "\t", rev, "\t",  merged # only for debug
        new_file_string = new_file_string+ merged
        
    
    print "Merged sequence will be:"
    print "-----------------------"
    print " "
    print new_file_string
    
    
    print " "
    out_filename = filename+".merged.fasta"
    print "Saving merged sequence to ", out_filename
    
    with open(out_filename, 'w') as file_out:
        file_out.write(new_file_string)    
    
    
    command = "mkdir merged && cp "+out_filename+" merged"
    
    print ">This command is executed:\n\t",command
    call(command, shell=True)
    #if not call(command, shell=True):
        #print "created dir 'merged'"
    #else:
    #    print "Making merged dir failed"
    
    print "Saving a copy of the merged sequence to merged/", out_filename
    with open("merged/"+out_filename, 'w') as file_out:
        file_out.write(new_file_string) 
        
if __name__ == '__main__':
    #print "len(sys.argv) = ", len(sys.argv) 
    if (len(sys.argv) == 1 or sys.argv[1] == '-h'):
        print '''
        aligne_and_correct_sequences.py  

        A script to correct aligend seqences from the package
        https://github.com/c-automate/sequence-editing-helpers
        by c-automate
        
        Usage: 
             ./aligne_and_correct_sequence.py filename1.fasta filename2.fasta
            
        This is a script that corrects the forward sequence using 
        information of the reverse complement. Therefore it takes a fasta file 
        with two sequences.
        It finds the reverse complement and then alignes it with the forward.
        This creates the intermediate "needle" file for review.
        From the aligned needle-file it creates the final merged file.

        
        Notes:
        ======
        
        You need to have emboss comand line installed to run "revseq" and 
        "needle". Emboss can be found at http://emboss.sourceforge.net/
        
        Make sure the original file only contains the forward and the 
        reverse complement (See Example1).
        
        The created needle file will contain two aligned sequences. 
        The forward sequence and the reverse complement.
        The the script will substitude ambigious bases of the 
        forward sequence by the information of the reverse
        complement and create the merged sequence.
    
        If the programm can't decide what to do it adds a "?" as base.
        All merged corrected sequences are saved in the directory 'merged'
        
        Example1: 
             ./aligne_and_correct_sequences.py example_data_raw.fasta

             cat example_data_raw.fasta
             >example_sequence_F
             AAGATATWWATATAKGATTTTCTAATGTGTTMAGGWKCAMGAAAGAWATGGATTKATCTG
             CAYTTCGCGTTGAAGAAGTACAAAATGTCATTAATG
             >example_sequence_R
             GATTTYCTGCAKAGSRTWARKGACWTTTMGKACTTCTKCRACGCGRAATGCARATAARTC
             CWTTTCKTTCGWGAACCTTWRSWCMTTAGAWRATCR
            
        Produces the following output:
                         
             ...
             Merged sequence will be:
             -----------------------
 
             >example_sequence_F_merged
             AAGATATWWATATA?GATTTTCTAATGTGTTAAGGTTCACGAAAGAAATGGATTTATCTGCATTTCGCGTTGAAGAAGTACAAAATGTCATTAATGCTMTGCAGRAAATC
 
             Saving merged sequence to  example_data_raw.fasta.needle.merged.fasta
             >This command is executed:
             	mkdir merged && cp example_data_raw.fasta.needle.merged.fasta merged
             mkdir: cannot create directory ‘merged’: File exists
             Saving a copy of the merged sequence to merged// example_data_raw.fasta.needle.merged.fasta

            
            
        Example2:
                ./aligne_and_correct_sequences.py *.fasta
        
        Processes all fasta files in the folder
            '''
        
    else:    
        for filename in sys.argv[1:]:
            
            aligned_file = create_aligned_file(filename)
            run_sequence_correction(aligned_file)
