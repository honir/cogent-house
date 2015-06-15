// -*- c -*-
#include "Filter.h"
#include "Packets.h"

configuration SensingC { 
  provides interface Read<bool> as SensingRead;
  provides interface AccessibleBitVector as Configured;
  provides interface PackState;
}

implementation
{
  components SensingP;
  SensingRead = SensingP.SensingRead;
  components new AccessibleBitVectorC(RS_SIZE) as MyConfigured; 
  
  Configured = MyConfigured;

  components HilTimerMilliC;
  SensingP.Configured -> MyConfigured;
  SensingP.LocalTime -> HilTimerMilliC;

  components SIPControllerC;

  components FilterM;
  components PredictC;
  

  components PassThroughC as Pass;

  components ThermalSensingM;
  components BatterySensingM;

  components new TimerMilliC() as HeartBeatTimer;
  components new HeartbeatC(HEARTBEAT_MULTIPLIER, HEARTBEAT_PERIOD);

  //Global SIP modules
  SIPControllerC.SinkStatePredict -> PredictC;
  HeartbeatC.HeartbeatTimer -> HeartBeatTimer;
  SIPControllerC.Heartbeat -> HeartbeatC;
  FilterM.LocalTime -> HilTimerMilliC;


  SensingP.ReadSensor[RS_TEMPERATURE] -> SIPControllerC.Sensor[RS_TEMPERATURE];
  SensingP.ReadSensor[RS_HUMIDITY] -> SIPControllerC.Sensor[RS_HUMIDITY];
  SensingP.ReadSensor[RS_VOLTAGE] -> SIPControllerC.Sensor[RS_VOLTAGE];
  SensingP.ReadSensor[RS_ADC_0] -> SIPControllerC.Sensor[RS_ADC_0];
  SensingP.ReadSensor[RS_ADC_1] -> SIPControllerC.Sensor[RS_ADC_1];
  SensingP.ReadSensor[RS_ADC_2] -> SIPControllerC.Sensor[RS_ADC_2];
  SensingP.ReadSensor[RS_ADC_3] -> SIPControllerC.Sensor[RS_ADC_3];
  SensingP.ReadSensor[RS_ADC_6] -> SIPControllerC.Sensor[RS_ADC_6];
  SensingP.ReadSensor[RS_ADC_7] -> SIPControllerC.Sensor[RS_ADC_7];
  SensingP.ReadSensor[RS_PAR] -> SIPControllerC.Sensor[RS_PAR];
  SensingP.ReadSensor[RS_TSR] -> SIPControllerC.Sensor[RS_TSR];
  SensingP.ReadSensor[RS_GIO2] -> SIPControllerC.Sensor[RS_GIO2];
  SensingP.ReadSensor[RS_GIO3] -> SIPControllerC.Sensor[RS_GIO3];

  // Temperature wiring
  FilterM.GetSensorValue[RS_TEMPERATURE]  -> ThermalSensingM.ReadTemp;
  FilterM.Filter[RS_TEMPERATURE] -> Pass.Filter[RS_TEMPERATURE];
  SIPControllerC.EstimateCurrentState[RS_TEMPERATURE]  -> FilterM.EstimateCurrentState[RS_TEMPERATURE];

  // Hum Wiring
  FilterM.GetSensorValue[RS_HUMIDITY]  -> ThermalSensingM.ReadHum;
  FilterM.Filter[RS_HUMIDITY]  -> Pass.Filter[RS_HUMIDITY];
  SIPControllerC.EstimateCurrentState[RS_HUMIDITY]  -> FilterM.EstimateCurrentState[RS_HUMIDITY];

  // Battery Wiring
  FilterM.GetSensorValue[RS_VOLTAGE]  -> BatterySensingM.ReadBattery;
  FilterM.Filter[RS_VOLTAGE]  -> Pass.Filter[RS_VOLTAGE];
  SIPControllerC.EstimateCurrentState[RS_VOLTAGE]  -> FilterM.EstimateCurrentState[RS_VOLTAGE];

  //Transmission Control
  SensingP.TransmissionControl -> SIPControllerC.TransmissionControl;




  //expectReadDone
  components new BitVectorC(RS_SIZE) as ExpectReadDone;
  SensingP.ExpectReadDone -> ExpectReadDone.BitVector;

  //PackState
  components new PackStateC(SC_SIZE) as MyPackState;
  PackState = MyPackState;
  components new AccessibleBitVectorC(SC_SIZE) as ABV;

  MyPackState.Mask -> ABV;
  SensingP.PackState -> MyPackState;

  //sensing interfaces
  components new SensirionSht11C();
  components new VoltageC() as Volt;


  //Wire up Sensing
  ThermalSensingM.GetTemp -> SensirionSht11C.Temperature;
  ThermalSensingM.GetHum ->SensirionSht11C.Humidity;
  BatterySensingM.GetVoltage -> Volt;


}

