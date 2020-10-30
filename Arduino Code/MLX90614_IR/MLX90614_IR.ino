/*

MLX90614      Arduinp
Vin         = 3.3v or 5v
Gnd         = Gnd
SCL         = A5
SDA         = A4

Download the library to include library for Adafruit

 
*/

#include <Wire.h>
#include <Adafruit_MLX90614.h>
char *typeName[]={"Object","Ambient"};

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

// defines pins numbers
const int trigPin = 9;
const int echoPin = 10;
// defines variables
long duration;
int distance;



void setup() {
 
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
 
  Serial.begin(9600);

  mlx.begin();  
}

void loop() {
  
  //printTemp('C');
  //printTemp('D');
  
  //printTemp('F');  
  //printTemp('G');
 
 // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance= duration*0.034/2;
  // Prints the distance on the Serial Monitor
  //Serial.print("Distance: ");
  //-Serial.println(distance);
  /* 
 if (distance<20)
 {
  if( getTemp('C')>40)
  {
    Serial.println("Temperature Excide");
    printTemp('K');   
    printTemp('C');  
    Serial.println("======");
  }
  else
  {
  Serial.println("Temperature Normal");
  printTemp('K');   
  printTemp('C');  
  //Serial.println("======");
  }
  
  //printTemp('K');   
  //printTemp('L');  
  //Serial.println("======");

  delay(3000);
  
 }
else{
 Serial.println("Come Closer");
 }
*/
//printTemp('K');   
printTemp('C');  
//Serial.println("======");
//delay(3000);
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
   // Robojax.com MLX90614 Code
  float value;
    float tempObjec = mlx.readObjectTempC();//in C object
    float tempAmbient = mlx.readAmbientTempC();
   if(type =='F')
   {
    value = mlx.readObjectTempF(); //Fah. Object
   }else if(type =='G')
   {
    value = mlx.readAmbientTempF();//Fah Ambient
   }else if(type =='K')
   {
    value = tempObjec + 273.15;// Object Kelvin
   }else if(type =='L')
   {
    value = tempAmbient + 273.15;//Ambient Kelvin
   }else if(type =='C')
   {
    value = tempObjec;
   }else if(type =='D')
   {
    value = tempAmbient;
   }
   return value;
    // MLX90614 Code
}//getTemp

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
  // Robojax.com MLX90614 Code
  float tmp =getTemp(type);
 /* 
   //Sameer edit
  if(type =='C')
  {
    Serial.print(typeName[0]);
    Serial.print(" ");    
    Serial.print(tmp);
    Serial.print("°");      
    Serial.println("C");
  }
  */

if(type =='C')
  {
   //Serial.println(tmp);
   Serial.print(tmp);
   Serial.print("\n");
   delay(1000);
  }
  
  else if(type =='D')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");     
    Serial.print(tmp);
    Serial.print("°");      
    Serial.println("C");
  }else if(type =='F')
  {
    Serial.print(typeName[0]);
    Serial.print(" ");     
    Serial.print(tmp);
    Serial.print("°");      
    Serial.println("F");
  }else if(type =='G')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");     
    Serial.print(tmp);
    Serial.print("°");      
    Serial.println("F");
  }

  else if(type =='K')
  {
    Serial.print(typeName[0]);
    Serial.print(" ");     
    Serial.print(tmp);  
    Serial.print("°");       
    Serial.println(" K");
  }  
  else if(type =='L')
  {
    Serial.print(typeName[1]);
    Serial.print(" ");     
    Serial.print(tmp);  
    Serial.print("°");       
    Serial.println(" K");
  }

// MLX90614 Code
}//printTemp(char type)
