module WallTempM
{
	provides 
	{
		interface Read<float> as ReadWallTemp;
	}
	uses
	{
		interface Read<uint16_t> as GetWallTemp;
	}
}
implementation
{
	const float vref=2.5;
	const float maxAdc=4095.0;

	//Temp1
	task void readTempTask()
	{
		call GetWallTemp.read();
	}

	command error_t ReadWallTemp.read()
	{
		post readTempTask();
		return SUCCESS;
	}

	//Convert raw adc to temp
	event void GetWallTemp.readDone(error_t result, uint16_t data) {
		float voltage;
		voltage=(data/maxAdc)*vref;
		signal ReadWallTemp.readDone(SUCCESS, voltage);
	}
}
