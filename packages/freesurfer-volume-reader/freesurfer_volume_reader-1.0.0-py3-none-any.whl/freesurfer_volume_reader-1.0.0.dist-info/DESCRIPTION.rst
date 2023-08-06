Read hippocampal subfield volumes computed by Freesurfer and/or ASHS

https://sites.google.com/site/hipposubfields/home
https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfields

>>> from freesurfer_volume_reader import ashs, freesurfer
>>>
>>> for volume_file in itertools.chain(
>>>         ashs.HippocampalSubfieldsVolumeFile.find('/my/ashs/subjects'),
>>>         freesurfer.HippocampalSubfieldsVolumeFile.find('/my/freesurfer/subjects')):
>>>     print(volume_file.absolute_path)
>>>     print(volume_file.subject, volume_file.hemisphere)
>>>     print(volume_file.read_volumes_mm3())
>>>     print(volume_file.read_volumes_dataframe())

