	jM??St??jM??St??!jM??St??	x5a3t'@x5a3t'@!x5a3t'@"e
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails$jM??St??Dio?????AZd;?O??Y????߮?*	?????T@2F
Iterator::ModelA??ǘ???!?+Q?K@)n????1?cp>?G@:Preprocessing2v
?Iterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate?? ?rh??!??+Q?4@)??H?}??1?????1@:Preprocessing2l
5Iterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat???Q???!KԮD?J2@)????????1}???|.@:Preprocessing2U
Iterator::Model::ParallelMapV2??_?Lu?!^?ڕ?]@)??_?Lu?1^?ڕ?]@:Preprocessing2Z
#Iterator::Model::ParallelMapV2::ZipU???N@??!?JԮD?F@)??H?}m?1?????@:Preprocessing2?
OIterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate[0]::TensorSlice??_?Le?!^?ڕ?]	@)??_?Le?1^?ڕ?]	@:Preprocessing2x
AIterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat::FromTensor{?G?zd?!dp>?c@){?G?zd?1dp>?c@:Preprocessing2f
/Iterator::Model::ParallelMapV2::Zip[0]::FlatMap??~j?t??!,Q??+7@)????Mb`?1??18?@:Preprocessing:?
]Enqueuing data: you may want to combine small input data chunks into fewer but larger chunks.
?Data preprocessing: you may increase num_parallel_calls in <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#map" target="_blank">Dataset map()</a> or preprocess the data OFFLINE.
?Reading data from files in advance: you may tune parameters in the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch size</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave cycle_length</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer_size</a>)
?Reading data from files on demand: you should read data IN ADVANCE using the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer</a>)
?Other data reading or processing: you may consider using the <a href="https://www.tensorflow.org/programmers_guide/datasets" target="_blank">tf.data API</a> (if you are not using it now)?
:type.googleapis.com/tensorflow.profiler.BottleneckAnalysis?
both?Your program is MODERATELY input-bound because 11.7% of the total step time sampled is waiting for input. Therefore, you would need to reduce both the input time and other time.no*high2t43.7 % of the total step time sampled is spent on 'All Others' time. This could be due to Python execution overhead.9y5a3t'@>Look at Section 3 for the breakdown of input time on the host.B?
@type.googleapis.com/tensorflow.profiler.GenericStepTimeBreakdown?
	Dio?????Dio?????!Dio?????      ??!       "      ??!       *      ??!       2	Zd;?O??Zd;?O??!Zd;?O??:      ??!       B      ??!       J	????߮?????߮?!????߮?R      ??!       Z	????߮?????߮?!????߮?JCPU_ONLYYy5a3t'@b 