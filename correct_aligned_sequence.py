#!/usr/bin/python
"""
This Created on Sun Jun 12 18:09:39 2016



Depencies:
==========
    * Depends on fasta.py from https://github.com/brentp/pyfasta
    

"""
import sys
from pyfasta.fasta import Fasta # Depends on fasta.py from https://github.com/brentp/pyfasta

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
        sys.exit(2)
        return
    
    print "Loded data from file: ", filename
    name_f_sequence = f.items()[0][0];
    print "name_f_sequence = ", name_f_sequence
    name_r_sequence = f.items()[1][0];
    print "name_r_sequence = ", name_r_sequence
    
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
        # print base_idx+1, "\t", forw,  "\t", rev, "\t",  merged # only for debug
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

if __name__ == '__main__':
    if (len(sys.argv) != 2 or sys.argv[1] == '-h'):
        print '''
        correct_aligned_sequence 

        A script to correct aligend seqences from the package
        https://github.com/c-automate/sequence-editing-helpers
        by c-automate
        
        Usage: 
             ./correct_aligned_sequence.py filename.fasta
            
        The fasta file hast to contain two aligned sequences. 
        The forward sequence and the flipped reverse sequence.
        The the script will substitude ambigious bases of the 
        forward sequence by the information of the flipped reverse
        sequence and create the merged sequence.

        License: MIT
        '''
        
    else:
        filename = sys.argv[1]
        run_sequence_correction(filename)
