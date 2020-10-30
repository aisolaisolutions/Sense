#include <Wire.h>
#include <Adafruit_MLX90614.h>
char *typeName[]={"Object","Ambient"};

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

void setup() {
  Serial.begin(9600);

  mlx.begin();  
}

void loop() {
  //Robojax Example for MLX90614
  printTemp('C');
  printTemp('D');
  
  printTemp('F');  
  printTemp('G'); 
  if( getTemp('C')>40)
  {
    //do something here
  }
  
  printTemp('K');   
  printTemp('L');  
  Serial.println("======");

  delay(3000);
  
}


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
   
}


void printTemp(char type)
{
  
  float tmp =getTemp(type);

  if(type =='C')
  {
    Serial.print(typeName[0]);
    Serial.print(" ");    
    Serial.print(tmp);
    Serial.print("°");      
    Serial.println("C");
  }else if(type =='D')
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

}
