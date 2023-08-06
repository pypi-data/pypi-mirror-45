from enum import unique
from datetime import datetime
from typing import List, Optional
from .message import Choice, ControlMessage, ControlRequest, Status, Session, \
                     datetimetype, hextype
from .typing import Object, fixedmember, member, optionalmember


class File(Object):
	name:   member[str] = member('FileName')
	disk:   member[int] = member('DiskNo')
	part:   member[int] = member('SerialNo')
	length: member[int] = member('FileLength', hextype)  # 2**10 bytes
	start:  member[Optional[datetime]] = member('BeginTime', datetimetype)
	end:    member[Optional[datetime]] = member('EndTime', datetimetype)


class GetFileReply(Object, ControlMessage):
	type = 1441

	status:  member[Status]  = member('Ret')
	command: member[str]     = member('Name')  # TODO
	session: member[Session] = member('SessionID')
	files:   optionalmember[List[File]] = optionalmember('OPFileQuery')


@unique
class FileType(Choice):
	VIDEO = 'h264'
	IMAGE = 'jpg'


class FileQuery(Object):
	start:   member[Optional[datetime]] = member('BeginTime', datetimetype)
	end:     member[Optional[datetime]] = member('EndTime', datetimetype)
	channel: member[int] = member('Channel')
	event:   fixedmember = fixedmember('Event', '*')  # TODO
	type:    member[FileType] = member('Type')


class GetFile(Object, ControlRequest):
	type = 1440
	reply = GetFileReply

	command:   fixedmember       = fixedmember('Name', 'OPFileQuery')
	session:   member[Session]   = member('SessionID')
	filequery: member[FileQuery] = member('OPFileQuery')
