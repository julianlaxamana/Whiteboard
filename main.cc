#include <wiringPi.h>
#include <iostream>
#include <unistd.h>
#include <chrono>
using namespace std;

extern "C" {
	// Assembly loop
	void asmLoop();

	// Setup pins in assembly
	void setup();

	// helper function for ultrasonic sensor
	int getDistance();
	void generateImage();

	void writePin(int pin, int mode);
	void hi(int test);
	void hsleep(int us);
}

void hi(int test){
	cout << test << endl;
}
void hsleep(int us){
	usleep(us);
}
void setup(){

}
void writePin(int pin, int mode){
	digitalWrite(pin, mode);
}

// Get the distance from Ultrasonic Sensor
int getDistance(){
		digitalWrite(25, LOW);
		usleep(2000);
		digitalWrite(25, HIGH);
		usleep(10000);
		digitalWrite(25, LOW);
		auto startTime = std::chrono::high_resolution_clock::now();
		auto stopTime = std::chrono::high_resolution_clock::now();

		while (digitalRead(24) == LOW) {
			startTime = std::chrono::high_resolution_clock::now();
		}
		while (digitalRead(24) == HIGH) {
			stopTime = std::chrono::high_resolution_clock::now();
		}

		auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stopTime - startTime).count();
		return duration / 29 / 2;
}
void generateImage(){
	system("python upload_bot.py");
}



int main(){
	wiringPiSetup();
	pinMode(25, OUTPUT);
	pinMode(0, OUTPUT);
	pinMode(24, INPUT);

	// Do assembly loop
	//asmLoop();
}
