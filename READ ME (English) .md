# Overall structure
**Please note that in order to distinguish between logical structure and physical structure, different terms will be used in the description:**

- **Unit -> Logical Architecture**
- **Original -> Physical Structure**

## Logical structure
In terms of logical design, the system is mainly composed of the following units:
- Acoustic stimulation unit
    - Acoustic stimulation power supply unit
    - Acoustic stimulation control unit
    - Acoustic stimulation unit
- Light stimulation unit
    - Acoustic stimulation power supply unit
    - Acoustic stimulation control unit
    - Acoustic stimulation unit
- Main control unit
    - Main control unit
    - Main control power supply unit

The two stimulation units are used to generate corresponding stimulation signals, and the main control unit is responsible for generating an operation interface readable by the experimenter, and after specifying the parameters, it coordinates the configuration of the two stimulation units and completes the recording of basic experimental data.

## Physical structure
In terms of physical realization, this system mainly consists of the following originals:

- Power supply element 
    - Master control and sound stimulation power supply
        > Corresponding logic structure: Acoustic stimulation power supply unit + main control power supply unit
    - Light stimulation power supply 
        > Corresponding logic structure: light stimulation power supply unit
- Controling element
    - Master controling element
        > Corresponding logic structure: main control unit
    - Acoustic stimulation controling unit 
        > Corresponding logic structure: Acoustic stimulation control unit
    - Light stimulation controling unit 
        > Corresponding logic sturcture: light stimulation control unit
- Irritation elements
    - Sound stimulation element 
        > Corresponding logic structure: Acoustic stimulation generating unit
    - Light stimulation element 
        > Corresponding logic structure: light stimulation generating unit

---

# Description of each element
**The following description mainly focuses on the physical elements.**

* The parameters involved in the section `Specification Requirements` must meet the specified requirements, and the parameters not mentioned should be determined according to the actual situation. *

## Power supply element 
The original power supply is mainly responsible for providing all the elements in the system with the power needed for their work.

Taking into account the diversity of power input, the following only requires the output related to power supply. Please determine the input terminal according to the actual situation, but here are some suggestions:
1. Try to ground the input terminal
2. Try to use the voltage and power commonly used in the experimental site for the input terminal

### Master control and sound stimulation power supply elements
#### Description
At the same time, power is supplied to the main control element and the acoustic stimulation control element. Since the acoustic stimulation control unit is highly integrated with the main control unit and its internal circuit has its own integrated power supply (the acoustic stimulation control unit has a built-in circuit that supplies power to the main control unit), in order to simplify the actual circuit, the two are combined for power supply. The actual wiring is that it is only necessary to connect the power supply element and the acoustic stimulation control element.

#### Specifications
- Output voltage: DC 12V
- Output power:> 40W
- Output interface: 5.5*2.5mm universal DC plug

### Light stimulation power supply element
#### Description
Considering that the voltage change of the light stimulation unit is relatively large, the power is relatively large, and the control circuit is relatively simple, an independent power supply is prepared for it.
#### Specifications
- Output voltage: DC 12V
- Output power: Determined according to the length of the light strip used
- Output interface: Just connect the jumper


## Controlling elements
The control element is mainly responsible for controlling the work of the underlying circuit element according to the received signal.

### Master control elements
#### Description
The main control uses Raspberry Pi 4B* (hereinafter referred to as Raspberry)*. The main process control software is running on it, which is responsible for generating an easy-to-read operation interface for the experimenter, and controlling the acoustic stimulation control element and the light stimulation control element connected to it according to the parameters given by the experimenter.

**Please note: In addition to the most basic circuit board, you also need to configure a microSD card for it. **

#### Specifications
 - Specific model: Raspberry Pi 4B
 - Memory capacity:> 1GB
 - MicroSD card capacity:> 16GB

### Acoustic stimulation control elements
#### Description
The voice control uses IQaudio DigiAMP+* (hereinafter referred to as IQaudio)*. Responsible for converting the digital sound signal sent by the master controller into an analog signal, and after amplifying it, it drives the original work of sound stimulation.

#### Specifications
Specific model: IQaudio DigiAMP+

### Light stimulation control element 
#### Description
The light stimulation control original is based on the circuit here(https://doi.org/10.1038/s41596-018-0021-x), please refer to the paper for details.




# Hardware construction instructions

## Tool list
- [ ] 1 electric soldering iron
- [ ] Several screwdrivers (please choose the head according to your needs)


## Consumables list
- [ ] USB Type-A plug to USB Type-B plug 1 data cable
- [ ] soldering tin
- [ ] Several jumpers
- [ ] fluxes
- [ ] Several insulating tapes

## Construction steps
### 1. Self-made circuit boards needed to make light stimulation control originals
> For specific requirements and steps, please refer to the content in [thesis link](https://doi.org/10.1038/s41596-018-0021-x)

### 2. Connect the homemade circuit board to the Arduino board
> The identification of the self-made circuit board in Figure 2b is still used here. [Thesis link](https://doi.org/10.1038/s41596-018-0021-x)
> Please refer to the figure below for details
> ![board](img/board.jpg)
-2.1 Connect the Ard + of the homemade circuit board to the 13 port of the Arduino board
-2.2 Connect the Ard GND of the homemade circuit board to the GND port of the Arduino board (Arduino has multiple GND ports, just connect to one of them)

### 3. Connect the self-made circuit board and the LED strip
> The identification of the self-made circuit board in [Thesis link](https://doi.org/10.1038/s41596-018-0021-x) Figure 2b is still used here
-3.1 Connect the LED + of the self-made circuit board to the positive pole of the LED strip
-3.2 Connect the LED GND of the self-made circuit board to the negative pole of the LED strip

### 4. Connect self-made circuit board and transformer (optical stimulation power supply original)
> The identification of the self-made circuit board in [Thesis link](https://doi.org/10.1038/s41596-018-0021-x) Figure 2b is still used here
-3.1 Connect the P + of the self-made circuit board to the positive output of the transformer (optical stimulation power supply unit)
-3.2 Connect the P GND of the self-made circuit board to the negative output of the transformer (light stimulation power supply unit)

### 5. Install the IQaudio board to the Raspberry board
> For specific requirements and steps, please refer to [iqaudio-product-brief](https://datasheets.raspberrypi.org/iqaudio/iqaudio-product-brief.pdf)

### 6. Connect the IQaudio board and the transformer (main control and sound stimulation power supply original)
Connect the transformer output port (5.5*2.5mm universal DC plug) to the power input port of the IQaudio board.

### 7. Connect the IQaudio board to the original sound stimulus

### 7. Connect Raspberry board and Arduino board
- 7.1 Take the USB Type-A plug to USB Type-B plug data cable and connect the Raspberry board (Type-A plug to the blue USB3.0 socket) and Arduino board RESET-B plug to the corresponding socket).

- 7.2 Connect Arduino RESET and Raspberry Wiringpi 21
- 7.3 Connect Arduino INPUT 8 and Raspberry Wiringpi 22
> There will be a clear port mark on the Arduino board, please refer to the figure below for the Raspberry board
> ![pinout](img/pinout.png)


# Software setting instructions
## Equipment List
- [ ] 1 computer (Internet connection required)
- [ ] USB Type-A plug to USB Type-B plug 1 data cable
- [ ] 1 microSD card reader
- [ ] Wi-Fi is required

## Setup steps

1. Install the Raspberry OS system on the microSD card
   > For details, see [Raspberry Pi Setup](https://www.raspberrypi.org/documentation/setup/)
2. Configure your own networking
3. Run the following command to upgrade the system
   ```
   # upgrade system
   sudo apt update
   sudo apt full-upgrade

   # upgrade eeprom
   sudo rpi-eeprom-update -a
   # rpi-eeprom-config --edit

   # upgrade wiringpi
   cd /tmp
   wget https://project-downloads.drogon.net/wiringpi-latest.deb
   sudo dpkg -i wiringpi-latest.deb
   cd-
   ```
4. Use git to download the code (project homepage https://github.com/WH-2099/Digital-Theraputics) and enter its directory
   ```
   git clone https://github.com/WH-2099/Digital-Theraputics.git
   cd Digital-Theraputics/
   ```
5. Run the following command to install the required dependencies
   ```
   sudo apt-get install -y python3-dev libasound2-dev
   sudo pip3 install -r requirements.txt
   ```

6. Upload the code under the project `arduino` to Arduino
   > For details, see [Getting Started with Arduino UNO](https://www.arduino.cc/en/Guide/ArduinoUno)

## Run steps
1. Enter the `Digital-Theraputics` directory
   ```
   cd Digital-Theraputics/
   ```
2. Start the main program
   ```
   python3 main.py
   ```


## Emergency closure
**1. Disconnect the power supply of the transformer connected to the LED strip**

**2. Disconnect the power supply of the transformer connected to the control board**

*Under normal circumstances, this operation will not cause damage to the hardware of the system, but some functions of the software (such as experimental data recording) may be damaged! *
