This is a converter from KiCad PCB to Protel ASCII Format. If you want to change the format of your Kicad file, you can use it. After conversion, you have a file `1.PcbDoc` which you can open it in Altium designer.

Here is the original PCB in KiCad:

![](https://github.com/yalda-amirsoleymani/kicad2protel/blob/master/kicad.png)

And this is converted file in Altium Designer:

![](https://github.com/yalda-amirsoleymani/kicad2protel/blob/master/protel.png)

It's pretty simple, just run the `kicad2protel.py` from command line and give your KiCad PCB filename as first argument, like below:

```bash
python3 kicad2protel.py KICADFILE
```

