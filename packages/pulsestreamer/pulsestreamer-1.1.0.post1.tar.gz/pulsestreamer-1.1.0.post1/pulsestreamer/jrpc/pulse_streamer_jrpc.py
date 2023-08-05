#import class Sequence and OutoutState for advanced sequence building
from pulsestreamer.sequence import  Sequence, OutputState

try:
    from tinyrpc import RPCClient
    from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
    from tinyrpc.transports.http import HttpPostClientTransport
except Exception as e:
    print(str(e))
    assert False, \
"""
Failed to import JSON-RPC library. Ensure that you have it installed by typing
> pip install tinyrpc or pip install tinyrpc --upgrade (ensure suppport of Python3)
> pip install gevent-websocket
in your terminal.
"""

# binary and base64 conversion
import struct
import base64
import six
import numpy as np

from pulsestreamer.enums import ClockSource, TriggerStart, TriggerRearm, Serial

class PulseStreamer():
    """
    Simple python wrapper for a PulseStreamer 8/2
    that describes sequences in the form of sequence steps as (time, [0,1,3], 0.8, -0.4),
    where time is an integer in ns (clock ticks),
    [0,1,3] is a list numbering the channels that should be high
    the last two numbers specify the analog outputs in volt.
    For advanced sequence creation use the method createSequence() and the functionality of
    the class Sequence described in the documentation of the Pulse Streamer 8/2.
    """
    REPEAT_INFINITELY=-1

    def __init__(self, ip_hostname='pulsestreamer'):
        print("Connect to Pulse Streamer via JSON-RPC.")
        print("IP / Hostname:", ip_hostname)
        url = 'http://'+ip_hostname+':8050/json-rpc'
        try:
            client = RPCClient(JSONRPCProtocol(), HttpPostClientTransport(url, timeout=20))
            self.proxy = client.get_proxy()
            try:
                self.proxy.getSerial()
            except:
                try:
                    self.proxy.isRunning()
                    assert False, "Pulse Streamer class not compatible with current firmware. Please update your firmware." \
                        "For detailed information visit https://www.swabianinstruments.com/pulse-streamer-8-2-firmware/ " \
                        "or contact support@swabianinstruments.com"
                except AssertionError:
                    raise
                except:
                    assert False, "No Pulse Streamer found at IP/Host-address: "+ip_hostname
        except AssertionError:
            raise
        except:
            assert False, "No Pulse Streamer found at IP/Host-address: "+ip_hostname

    def reset(self):
        return self.proxy.reset()
        
    def constant(self, state=OutputState.ZERO()):
        if isinstance(state, OutputState):
            state=state.getData()
            output=(0, state[0], state[1], state[2])
        else:
            output = self.convert_sequence_step((0, state[0], state[1], state[2]))
        self.proxy.constant(output)

    def forceFinal(self):
        return self.proxy.forceFinal()
    
    def createOutputState(self, digi, A0=0.0, A1=0.0):
        output=OutputState(digi=digi,A0=A0, A1=A1)
        return output

    def createSequence(self): #ToDo parameter for safe communication/sequence creation
        seq = Sequence()
        return seq
        
    def stream(self, seq, n_runs=REPEAT_INFINITELY, final=OutputState.ZERO()):
        
        if isinstance(final, OutputState):
            state=final.getData()
            final =(0, state[0], state[1], state[2])
        else:
            final = self.convert_sequence_step((0, final[0], final[1], final[2]))

        if six.PY2:
            if isinstance(seq, Sequence):
                s = self.enc(seq.getData())
            else:
                s = self.enc(seq)
        else:
            if isinstance(seq, Sequence):
                s = self.enc(seq.getData()).decode("utf-8")
            else:
                s = self.enc(seq).decode("utf-8")
        
        self.proxy.stream(s, n_runs, final)

    def isStreaming(self):
        return self.proxy.isStreaming()

    def hasFinished(self):
        return self.proxy.hasFinished()

    def hasSequence(self):
        return self.proxy.hasSequence()

    def startNow(self):
        return self.proxy.startNow()

    def getUnderflow(self):
        return self.proxy.getUnderflow()

    def getDebugRegister(self):
        return self.proxy.getDebugRegister()

    def selectClock(self, source):
        if not isinstance(source, ClockSource):
            raise TypeError("source must be an instance of ClockSource Enum")
        else:
            return self.proxy.selectClock(source.value)

    def getFirmwareVersion(self):
        return self.proxy.getFirmwareVersion()

    def getSerial(self):
            return self.proxy.getSerial(Serial.MAC.name)
    
    def getFPGAID(self):
            return self.proxy.getSerial(Serial.ID.name)
    
    def setTrigger(self, start, rearm=TriggerRearm.AUTO):
        if not isinstance(start, TriggerStart):
            raise TypeError("start must be an instance of TriggerStart Enum")
        else:
            if not isinstance(rearm, TriggerRearm):
                raise TypeError("mode must be an instance of TriggerRearm Enum")
            else:
                return self.proxy.setTrigger(start.value, rearm.value)

    def setNetworkConf(self, ip, netmask, gateway):
        return self.proxy.setNetworkConf(ip, netmask, gateway)

    def getNetworkConf(self):
        return self.proxy.getNetworkConf()

    def testNetworkConf(self):
        return self.proxy.testNetworkConf()
        
    def enableStaticIP(self, permanent=False):
        assert permanent in [True, False]
        return self.proxy.enableStaticIP(permanent)

    def rearm(self):
        return self.proxy.rearm()

    def dec(self, b64):
        sdec = base64.b64decode(b64)
        import struct
        fmt = '>' + len(sdec)//3//3*'IBhh'
        s = struct.Struct(fmt)
        res = s.unpack(sdec)          
        return res
        
    def enc(self, seq):
        """
        Convert a human readable python sequence to a base64 encoded string and split sequence steps with duration exceeding limit of unsigned int
        """
        s = b''
        convert_list = []
        if type(seq[0][1])== list:
            for sequence_step in seq:
                if sequence_step[0] > 0xffffffff:
                    mod=sequence_step[0]%0xffffffff
                    count=sequence_step[0]//0xffffffff
                    for i in range(count):
                        sequence_step = (0xffffffff, sequence_step[1], sequence_step[2], sequence_step[3])
                        convert_list.extend(self.convert_sequence_step(sequence_step))
                    else:
                        sequence_step = (mod, sequence_step[1], sequence_step[2], sequence_step[3])
                convert_list.extend(self.convert_sequence_step(sequence_step))    
        else:
            for sequence_step in seq:
                if sequence_step[0] > 0xffffffff:
                    mod=sequence_step[0]%0xffffffff
                    count=sequence_step[0]//0xffffffff
                    for i in range(count):
                        sequence_step = (0xffffffff, sequence_step[1], sequence_step[2], sequence_step[3])
                        convert_list.extend(sequence_step)
                    else:
                        sequence_step = (mod, sequence_step[1], sequence_step[2], sequence_step[3])
                convert_list.extend(sequence_step)

        assert len(convert_list)//4<=2e6, "The resulting sequence length exceeds the limit of two million sequnence steps"

        fmt = '>' + len(convert_list)//4*'IBhh'
        s=struct.pack(fmt, *convert_list)  
        return base64.b64encode(s)
    
    def convert_sequence_step(self, sequence_step):
        t, chans, a0, a1 = sequence_step
        assert (abs(a0)<=1 and abs(a1)<=1), "Pulse Streamer 8/2 supports "\
                "analog voltage range of +/-1V" #check hardware
        assert t>=0
        return (t, self.chans_to_mask(chans), int(round(0x7fff*a0)), int(round(0x7fff*a1)))

    def chans_to_mask(self, chans):
        mask = 0
        for chan in chans:
            assert chan in range(8),"Pulse Streamer 8/2 supports "\
            "up to eight digital channels"
            mask |= 1<<chan
        return mask
        
"""---------Test-Code-------------------------------"""

if __name__ == '__main__':
    pulser = PulseStreamer(ip_hostname='pulsestreamer')

    print("Serial number:", pulser.getSerial())
    print("Firmware Version:", pulser.getFirmwareVersion())
