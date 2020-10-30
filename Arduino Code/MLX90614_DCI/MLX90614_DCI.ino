/*************************************************** 
  This is a library example for the MLX90614 Temp Sensor
Original Library and code source: https://github.com/adafruit/Adafruit-MLX90614-Library

The is Arduino code used from the above library for MLX90614 and have been updated heavily.
this code to use MLX90614-DCI the long range medical accuracy infrared Temperature sensor to measure
the temperature with accuracy and compensation of power supply dependancey. 
Please watch the video for details. We will acheive up to 20cm to 49cm readin range where the 
object size becomes 4.3cm  or 43mm.

 * 
 * Watch video instructions for this code: https://youtu.be/jN86PSAHMbw
updated/written by Ahmad Shamshiri on July 18, 2020, 2020 
 
 * in Ajax, Ontario, Canada. www.robojax.com
 * 

 * Get this code and other Arduino codes from Robojax.com
Learn Arduino step by step in structured course with all material, wiring diagram and library
all in once place. Purchase My course on Udemy.com http://robojax.com/L/?id=62

If you found this tutorial helpful, please support me so I can continue creating 
content like this. You can support me on Patreon http://robojax.com/L/?id=63

or make donation using PayPal http://robojax.com/L/?id=64

 *  * This code is "AS IS" without warranty or liability. Free to be used as long as you keep this note intact.* 
 * This code has been download from Robojax.com
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Origin
  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/
const int votageInputPin =A0;
const float arduinoVoltage = 5.0;//Operating voltage of Arduino. either 3.3V or 5.0V 
#include <Wire.h>
#include <Adafruit_MLX90614.h>
char *typeName[]={"Object","Ambient"};

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

float tempObjecC, tempObjecF, tempAmbientC ,tempAmbientF, tempObjecK, tempAmbientK;

void setup() {
  Serial.begin(9600);

  //Serial.println("Robojax MLX90614 test");  

  mlx.begin();  
}

void loop() {
  //Robojax Example for MLX90614-DCI medical accuracy long range version
  printTemp('C');
//  printTemp('D');
//  
//  printTemp('F');  
//  printTemp('G'); 
 // if( getTemp('C')>40)
 // {
    //do something here
 // }
  
//  printTemp('K');   
//  printTemp('L');  
 // Serial.println("======");
  //printVoltage();// this line will read the input voltage and dispalys it on serial monitor
  delay(2000);
  //Robojax Example for MLX90614-DCI medical accuracy long range version
}

/*
 * @brief returns temperature or relative humidity
 * @param "type" is character
 *     C = Object Celsius
 *     D = Ambient Celsius
 *     
 *     K = Object Keliven
 *     L = Ambient in Keilven
 *     
 *     F = Object Fahrenheit
 *     G = Ambient in Fahrenheit

 * @return returns one of the values above
 * Usage: to get Fahrenheit type: getTemp('F')
 * to print it on serial monitor Serial.println(getTemp('F'));
 * Written by Ahmad Shamshiri on Mar 30, 2020. 
 * in Ajax, Ontario, Canada
 * www.Robojax.com 
 */
float getTemp(char type)
{
   //Robojax Example for MLX90614-DCI medical accuracy long range version
  float value;
   tempObjecC = mlx.readObjectTempC();//in C object
   tempAmbientC = mlx.readAmbientTempC();

   tempObjecF = mlx.readObjectTempF(); //Fah. Object
   tempAmbientF = mlx.readAmbientTempF();//Fah Ambient

    dependencyComp();
      
   if(type =='F')
   {
    value = tempObjecF;
   }else if(type =='G')
   {
    value = tempAmbientF;
   }else if(type =='K')
   {
    value = tempObjecC + 273.15;// Object Kelvin
   }else if(type =='L')
   {
    value = tempAmbientC + 273.15;//Ambient Kelvin
   }else if(type =='C')
   {
    value = tempObjecC;
   }else if(type =='D')
   {
    value = tempAmbientC;
   }
   return value;
    //Robojax Example for MLX90614-DCI medical accuracy long range version
}//getTemp


/*
 * fixes the voltage dependancey of measurement
 * This funciton updates the reading of temperature by reading 
 * the power supply voltage and compensating it.
 * see page 37 of datasheet here: https://robojax.com/learn/arduino/robojax_MLX90614_Datasheet-Melexis.pdf
 * T=T0 - (VCC-3) *0.6
 */
void dependencyComp()
{
  //Robojax Example for MLX90614-DCI medical accuracy long range version
  int value = analogRead(votageInputPin);// read the input
  float voltage =  value * (arduinoVoltage / 1023.0);//get the voltage from the value above
  //Serial.println(voltage);
  tempObjecC = tempObjecC - (voltage -3) * 0.6;
  //tempObjecC;
  tempAmbientC = tempAmbientC - (voltage -3) * 0.6;  

  tempObjecF = tempObjecF - (voltage -3) * 0.6;
  tempAmbientF = tempAmbientF - (voltage -3) * 0.6;    

  tempObjecK = tempObjecK - (voltage -3) * 0.6;
  tempAmbientK = tempAmbientK - (voltage -3) * 0.6;     
  //Robojax Example for MLX90614-DCI medical accuracy long range version
}//dependencyComp() ends here


/*
 * @brief nothing
 * @param "type" is character
 *     C = Object Celsius
 *     D = Ambient Celsius
 *     
 *     K = Object Keliven
 *     L = Ambient in Keilven
 *     
 *     F = Object Fahrenheit
 *     G = Ambient in Fahrenheit

 * @return prints temperature value in serial monitor
 * Usage: to get Fahrenheit type: getTemp('F')
 * to print it on serial monitor Serial.println(getTemp('F'));
 * Written by Ahmad Shamshiri on Mar 30, 2020 at 21:51
 * in Ajax, Ontario, Canada
 * www.Robojax.com 
 */
void printTemp(char type)
{
  //Robojax Example for MLX90614-DCI medical accuracy long range version
  float tmp =getTemp(type);

  if(type =='C')
  {
    //Serial.print(typeName[0]);
    //Serial.print(" ");    
    Serial.print(tmp);
    Serial.print("\n");
    //printDegree();     
    //Serial.println("C");
  }else if(type =='D')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");     
    Serial.print(tmp);
    printDegree();     
    Serial.println("C");
  }else if(type =='F')
  {
    Serial.print(typeName[0]);
    Serial.print(" ");     
    Serial.print(tmp);
    printDegree();     
    Serial.println("F");
  }else if(type =='G')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");     
    Serial.print(tmp);
    printDegree();      
    Serial.println("F");
  }

  else if(type =='K')
  {
    Serial.print(typeName[0]);
    Serial.print(" ");     
    Serial.print(tmp);  
    printDegree();      
    Serial.println(" K");
  }  
  else if(type =='L')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");     
    Serial.print(tmp);  
    printDegree();      
    Serial.println(" K");
  }

//Robojax Example for MLX90614-DCI medical accuracy long range version
}//printTemp(char type)

/*
 * printDegree()
 * prints degree symble on serial monitor
 * written by Ahmad Shamshiri for Robojax.com 
 * 
 */
void printDegree()
{
     Serial.print("\xC2\xB0");     
}

/*
 *  printVoltage()
 *  prints voltage at pin "voltageInputPin"
 *  on serial monitor.
 */
void printVoltage()
{
  //Robojax Example for MLX90614-DCI medical accuracy long range version
  int value = analogRead(votageInputPin);// read the input
  float voltage =  value * (arduinoVoltage / 1023.0);//get the voltage from the value above
  Serial.print("Voltage: ");
  Serial.print(voltage);  
  Serial.println("V");
  //Robojax Example for MLX90614-DCI medical accuracy long range version
}// printVoltage()

 
 
