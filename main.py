#!/usr/bin/env python3.8

'''
          ;               ,           
         ,;                 '.         
        ;:                   :;        
       ::                     ::       
       ::                     ::       
       ':                     :        
        :.                    :        
     ;' ::                   ::  '     
    .'  ';                   ;'  '.    
   ::    :;                 ;:    ::   
   ;      :;.             ,;:     ::   
   :;      :;:           ,;"      ::   
   ::.      ':;  ..,.;  ;:'     ,.;:   
    "'"...   '::,::::: ;:   .;.;""'    
        '"""....;:::::;,;.;"""         
    .:::.....'"':::::::'",...;::::;.   
   ;:' '""'"";.,;:::::;.'""""""  ':;   
  ::'         ;::;:::;::..         :;  
 ::         ,;:::::::::::;:..       :: 
 ;'     ,;;:;::::::::::::::;";..    ':.
::     ;:"  ::::::"""'::::::  ":     ::
 :.    ::   ::::::;  :::::::   :     ; 
  ;    ::   :::::::  :::::::   :    ;  
   '   ::   ::::::....:::::'  ,:   '   
    '  ::    :::::::::::::"   ::       
       ::     ':::::::::"'    ::       
       ':       """""""'      ::       
        ::                   ;:        
        ':;                 ;:"        
-scrapy-  ';              ,;'          
            "'           '"            
              '
'''



import curses
import os

def main(win):
    win.nodelay(True)
    key=""
    win.clear()                
    win.addstr("Detected key:")
    while 1:          
        try:                 
            key = win.getkey()         
            win.clear()                
            win.addstr("Detected key:")
            win.addstr(str(key)) 
            if key == 'q':
                break           
        except Exception as e:
            # No input   
            pass 

curses.wrapper(main)


