import wiringPiNim
import strformat
import strutils
import os

const
  TIP = 14
  RING = 15
 
type
  VarType = enum
    VT_RealNum = 0x00'u8
    VT_RealList
    VT_Matrix
    VT_YVar
    VT_String
    VT_Program
    VT_LockedProgram
    VT_Pic
    VT_GDB
    VT_WindowName = 0x0b
    VT_CplxNum
    VT_CplxList
    VT_Window = 0x0F
    VT_SavedWindow
    VT_TableSetup
    VT_Backup = 0x13
    VT_AppVar = 0x15
    VT_Group = 0x17
    VT_Dir = 0x19

if piSetupGPIO() < 0:
  echo ":("
  quit()

proc sendByte(byte: uint8) =
  var data = byte
  for i in 1..8:
    var bit = (data and 1) != 0
    data = data shr 1
    while (piDigitalRead(TIP) == 0 or piDigitalRead(RING) == 0): discard
    var
      ourLine: cint
      oppositeLine: cint
    if (bit):
      ourLine = TIP
      oppositeLine = RING
    else:
      ourLine = RING
      oppositeLine = TIP
    piPinModeOutput(ourLine)
    piDigitalWrite(ourLine, 0)
    while piDigitalRead(oppositeLine) == 1: discard
    piPinModeInput(ourLine)
    piPullOff(ourLine)



proc getByte(): uint8 =
  for i in 1..8:
    while piDigitalRead(TIP) == 1 and piDigitalRead(RING) == 1: discard
    var
      ourLine: cint
      oppositeLine: cint
      bit = piDigitalRead(RING) == 0
    result = result shr 1
    if (bit):
      ourLine = TIP
      oppositeLine = RING
    else:
      ourLine = RING
      oppositeLine = TIP
      result = result or 128
    piPinModeOutput(ourLine)
    piDigitalWrite(ourLine, 0)
    while piDigitalRead(oppositeLine) == 0: discard
    piPinModeInput(ourLine)
    piPullOff(ourLine)

var currentType: VarType
var currentName: string

var currentBuffer: uint8 

var sendProgNext: string

proc sendProg(name: string) =
  var
    f = open(&"/home/pi/storage/{currentBuffer.toHex()}/{name}.prg", fmRead)
    data = readAll(f)
  f.close()

  sendByte(0x03)
  sendByte(0xC9)
  sendByte(0x0D)
  sendByte(0x00)
  echo "RPI: RTS"

  var cs = ((len(data) + 2) and 0xff).uint16
  cs += ((len(data) + 2)shr 8).uint8
  sendByte((len(data) + 2).uint8)
  sendByte(((len(data) + 2) shr 8).uint8)
  cs += VT_Program.uint16
  sendByte(VT_Program.uint8)
  for b in 0..7:
    try:
      sendByte(name[b].uint8)
      cs += name[b].uint8
    except:
      sendByte(0x00)
  sendByte(0x00)
  sendByte(0x00)

  sendByte((0xff and cs).uint8)
  sendByte((cs shr 8).uint8)

  discard getByte().toHex()
  var command = getByte()
  discard getByte().toHex()
  discard getByte().toHex()
  
  if command != 0x56:
    echo "error"
  echo "CLC: ACK"
  
  discard getByte().toHex()
  command = getByte()
  discard getByte().toHex()
  discard getByte().toHex()
  
  if command != 0x09:
    echo "error"
  echo "CLC: CTS"

  sendByte(0x03)
  sendByte(0x56)
  sendByte(0x00)
  sendByte(0x00)
  echo "RPI: ACK"
  
  sendByte(0x03)
  sendByte(0x15)
  sendByte((len(data) + 2).uint8)
  sendbyte(((len(data) + 2) shr 8).uint8)
  cs = (len(data)).uint8
  cs += (len(data) shr 8).uint8
  sendByte((len(data)).uint8)
  sendbyte(((len(data)) shr 8).uint8)
  for b in data:
    cs += b.uint16
    sendByte(b.uint8)
  sendByte((0xff and cs).uint8)
  sendByte((cs shr 8).uint8)
  echo "RPI: DAT"
  
  discard getByte().toHex()
  command = getByte()
  discard getByte().toHex()
  discard getByte().toHex()
  if command != 0x56:
    echo "error"
  echo "CLC: ACK"
  
  sendByte(0x03)
  sendByte(0x92)
  sendByte(0x00)
  sendByte(0x00)
  echo "RPI: EOT"

proc decodeData(data: seq[uint8]) =
  case currentType
  of VT_String:
    var text = ""
    for c in data[2..^1]:
      text &= c.char
    if currentName == "\xAA":
      try:
        currentBuffer = fromHex[uint8](text)
      except:
        sendProgNext = text
  of VT_Program:
    var text = ""
    for c in data[2..^1]:
      text &= c.char
    writeFile(&"/home/pi/storage/{currentBuffer.toHex()}/{currentName}.prg", text)
    echo &"Saved Program: {currentName}"
  else:
    echo currentType

proc decodeVar(data: seq[uint8]) =
  var dataSize = data[0].uint16 or (data[1] shl 8)
  var dataType = data[2]
  var i = 3
  var cur = data[i]
  var dataName = ""
  currentName = ""
  while cur != 0x00:
    dataName &= "\\x" & cur.toHex()
    currentName &= cur.char
    i += 1
    cur = data[i]
  currentType = dataType.VarType

  echo &"VarHeader {dataType.VarType}, size {dataSize}b, name '{dataName}'"

piPinModeInput(TIP)
piPinModeInput(RING)

piPullOff(TIP)
piPullOff(RING)

for i in 0..255:
  createDir(&"/home/pi/storage/{i.uint8.toHex()}")

while true:
  discard getByte().toHex()
  var command = getByte()
  var dataSize = getByte().uint16
  dataSize = dataSize or (getByte() shl 8)
  case command:
  of 0x06:
    var data: seq[uint8]
    for d in 0..<dataSize.int:
      data &= getByte()
    var cs = getByte()
    cs = cs or (getByte() shl 8)
    echo "CLC: VAR"
    sendByte(0x73)
    sendByte(0x56)
    sendByte(0x00)
    sendByte(0x00)
    echo "RPI: ACK"
    sendByte(0x73)
    sendByte(0x09)
    sendByte(0x00)
    sendByte(0x00)
    echo "RPI: CTS"
    decodeVar(data)
  of 0x15:
    var data: seq[uint8]
    for d in 0..<dataSize.int:
      data &= getByte()
    var cs = getByte()
    cs = cs or (getByte() shl 8)
    echo "CLC: DAT"
    sendByte(0x73)
    sendByte(0x56)
    sendByte(0x00)
    sendByte(0x00)
    echo "RPI: ACK"
    decodeData(data)
  of 0x56:
    echo "CLC: ACK"
  of 0x92:
    echo "CLC: EOT"
    sendByte(0x73)
    sendByte(0x56)
    sendByte(0x00)
    sendByte(0x00)
    echo "RPI: ACK"
    if sendProgNext != "":
      try:
        echo &"send {sendProgNext}"
        sendProg(sendProgNext)
      except:
        echo &"Program {sendProgNext} NonExistant"
      sendProgNext = ""
  else:
    echo &"CLC: {command.toHex()}"
    sendByte(0x73)
    sendByte(0x56)
    sendByte(0x00)
    sendByte(0x00)
    echo "RPI: ACK"
