#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime

# ==== OSAID COLORS ====
RED = '\033[1;31m'
MAGENTA = '\033[1;35m'
CYAN = '\033[1;36m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
WHITE = '\033[1;37m'
RESET = '\033[0m'

def show_banner():
    os.system('clear')
    print(f"""{RED}
          ______                                
        .-'      `-.                            
       /            \\                           
      |              |                          
      |,  .-.  .-.  ,|                          
      | )(_o/  \\o_)( |                          
      |/     /\\     \\|                          
      (_     ^^     _)                          
   _____\\__      __/_____                       
  /      \\_`----'_/      \\                      
 /   /\\    `----'    /\\   \\                     
/   /  \\            /  \\   \\                    
\\  /    \\          /    \\  /                    
 \\/      \\        /      \\/                     
          \\      /                              
           \\    /                               
            \\  /                                
             \\/                                 
{MAGENTA}  ===================================================={RESET}
{CYAN}     [!] OSAID EXIF MASTER v7.0 - ULTIMATE ANALYZER [!]{RESET}
{MAGENTA}  ===================================================={RESET}
{GREEN}  [*] HACK THE PLANET. TRUST NO ONE. EXTRACT EVERYTHING.{RESET}
{YELLOW}  [*] Author: OSAID{RESET}
{MAGENTA}  ===================================================={RESET}
""")

def convert_to_degrees(value):
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

def get_gps_coords(gps_info):
    lat, lon = None, None
    if not gps_info: return None, None
    
    gps_data = {}
    for key, value in gps_info.items():
        name = GPSTAGS.get(key, key)
        gps_data[name] = value

    if 'GPSLatitude' in gps_data and 'GPSLongitude' in gps_data:
        lat = convert_to_degrees(gps_data['GPSLatitude'])
        lon = convert_to_degrees(gps_data['GPSLongitude'])
        
        if gps_data.get('GPSLatitudeRef') == 'S':
            lat = -lat
        if gps_data.get('GPSLongitudeRef') == 'W':
            lon = -lon
            
    return lat, lon

def analyze_image(image_path):
    print(f"\n{YELLOW}[*] SCANNING TARGET: {WHITE}{image_path}{RESET}\n")
    
    try:
        # 1. File Info
        file_size = os.path.getsize(image_path) / 1024
        mod_time = datetime.fromtimestamp(os.path.getmtime(image_path))
        
        print(f"{CYAN}[+] === FILE INFO ==={RESET}")
        print(f"  {GREEN}Size{RESET}: {WHITE}{file_size:.2f} KB{RESET}")
        print(f"  {GREEN}Last Modified{RESET}: {WHITE}{mod_time}{RESET}\n")

        # 2. Image Info
        image = Image.open(image_path)
        ratio = round(image.size[0] / image.size[1], 2)
        
        print(f"{CYAN}[+] === IMAGE INFO ==={RESET}")
        print(f"  {GREEN}Format{RESET}: {image.format}")
        print(f"  {GREEN}Dimensions{RESET}: {image.size[0]}x{image.size[1]}")
        print(f"  {GREEN}Aspect Ratio{RESET}: {ratio}")
        print(f"  {GREEN}Mode{RESET}: {image.mode}\n")

        # 3. EXIF
        exif_data = image._getexif()
        if not exif_data:
            print(f"{RED}[-] NO EXIF DATA FOUND.{RESET}")
            return

        print(f"{CYAN}[+] === EXIF METADATA ==={RESET}")
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag in ['GPSInfo', 'MakerNote', 'UserComment', 'ComponentsConfiguration']:
                continue 
            print(f"  {GREEN}{tag}{RESET}: {WHITE}{value}{RESET}")

        # 4. GPS
        gps_info = exif_data.get(34853)
        lat, lon = get_gps_coords(gps_info)
        
        if lat and lon:
            print(f"\n{MAGENTA}[!] === GPS LOCATION BREACHED ==={RESET}")
            print(f"  {GREEN}Latitude{RESET}:  {WHITE}{lat}{RESET}")
            print(f"  {GREEN}Longitude{RESET}: {WHITE}{lon}{RESET}")
            print(f"  {YELLOW}Google Maps{RESET}: https://www.google.com/maps?q={lat},{lon}")
            print(f"{MAGENTA}[!] ============================={RESET}")
        else:
            print(f"\n{RED}[-] NO GPS DATA FOUND.{RESET}")

        print(f"\n{GREEN}[+] SCAN COMPLETE. STAY DANGEROUS.{RESET}")

    except Exception as e:
        print(f"{RED}[-] SYSTEM FAILURE: {e}{RESET}")

if __name__ == "__main__":
    show_banner()
    while True:
        print(f"{YELLOW}[?] Enter Image Path (or 'exit' to quit): {RESET}", end="")
        image_path = input().strip()
        
        if image_path.lower() == 'exit':
            print(f"{RED}[!] Exiting...{RESET}")
            sys.exit()
        if not image_path:
            print(f"{RED}[-] Path cannot be empty.{RESET}\n")
            continue
        if not os.path.exists(image_path):
            print(f"{RED}[-] File not found: {image_path}{RESET}\n")
            continue
            
        analyze_image(image_path)
        break