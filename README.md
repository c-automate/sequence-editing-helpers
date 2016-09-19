==========================
 Sequence Editing Helpers
==========================

This package provides small python scripts that help with sequence editing.

Author: c-automate

__Available Helpers__

* aligne_and_correct_sequence
* correct_aligned_sequence


License
-----------

[MIT license](LICENSE)


Third Party Libraries
---------------------

This project is using [pyfasta](https://github.com/brentp/pyfasta) from
 commit c2f0611 on 1 Aug 2014 to load the fasta files.



Aligne And Correct Sequences
============================
            
This is a script that corrects the forward sequence using 
information of the reverse complement. Therefore it takes a fasta file 
with two sequences.
It finds the reverse complement and then alignes it with the forward.
This creates the intermediate "needle" file for review.
From the aligned needle-file it creates the final merged file.
        
Notes:
------

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
All merged corrected sequences are saved in the directory 'finals'.      
        
Installation:
-------------

Just copy the files on your local drive.


Usage: 
------
             ./aligne_and_correct_sequence.py filename1.fasta filename2.fasta
             
Example1: 
---------
Running the script with example data:

            ./aligne_and_correct_sequences.py example_data_raw.fasta
            
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
             Saving a copy of the merged sequence to merged/ example_data_raw.fasta.needle.merged.fasta

             
To see the used example data type

             cat example_data_raw.fasta
             
This will show the following:

             >example_sequence_F
             AAGATATWWATATAKGATTTTCTAATGTGTTMAGGWKCAMGAAAGAWATGGATTKATCTG
             CAYTTCGCGTTGAAGAAGTACAAAATGTCATTAATG
             >example_sequence_R
             GATTTYCTGCAKAGSRTWARKGACWTTTMGKACTTCTKCRACGCGRAATGCARATAARTC
             CWTTTCKTTCGWGAACCTTWRSWCMTTAGAWRATCR            
Example2: 
---------
Processes all fasta files in the folder

            ./aligne_and_correct_sequences.py *.fasta




Correct Aligned Sequence
========================

This is a script to correct aligend seqences in the fasta format.
The fasta file hast to contain two aligned sequences. The forward sequence and the flipped reverse sequence. The the script will substitude ambigious bases of the forward sequence by the information of the flipped reverse sequence and create the final sequence.

Installation:
-------------

Just copy the files on your local drive.

Usage: 
------
		./correct_aligned_sequence.py filename.fasta


Example: 
--------

To run a test just type the following commands in you linux terminal:

		./correct_aligned_sequence.py example_data_aligned.fasta

Detailed description:

                ./correct_aligned_sequence.py   # <- this is the command
                 # (Tab the "Tab" key for automatic completion)
                 # followed by the name of the aligned fasta file

This will create a new fasta file called `example_data_aligned.fasta.merged.fasta` that contains the corrected, final sequence.




