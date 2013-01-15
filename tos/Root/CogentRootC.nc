// -*- c -*-
#include "../Packets.h"
configuration CogentRootC { }
implementation
{
  components CogentRootP, MainC, LedsC;
  components SerialActiveMessageC as Serial;
  components ActiveMessageC as Radio;
  components new SerialAMReceiverC(AM_ACKMSG) as AckReceiver;
  components new AMSenderC(AM_ACKMSG) as RadioSend;
  components new AMReceiverC(AM_STATEMSG) as SMReceive;
  components new AMReceiverC(AM_BNMSG) as BNReceive;

  CogentRootP.Boot -> MainC;

  CogentRootP.SerialControl -> Serial;
  CogentRootP.UartSend -> Serial;
  CogentRootP.UartPacket -> Serial;
  CogentRootP.UartAMPacket -> Serial;
  CogentRootP.UartAckReceive -> AckReceiver;

  CogentRootP.RadioControl -> Radio;

  CogentRootP.Leds -> LedsC;

  CogentRootP.RadioSend -> RadioSend;
  CogentRootP.SMRadioReceive -> SMReceive;
  CogentRootP.BNRadioReceive -> BNReceive;
  CogentRootP.RadioPacket -> Radio;
  CogentRootP.RadioAMPacket -> Radio;

  components new QueueC(message_t*, SERIAL_QUEUE_SIZE);
  components new PoolC(message_t, SERIAL_QUEUE_SIZE);
  CogentRootP.Queue -> QueueC;
  CogentRootP.Pool -> PoolC;
	
  components new TimerMilliC() as BlinkTimer;
  CogentRootP.BlinkTimer -> BlinkTimer;

}
