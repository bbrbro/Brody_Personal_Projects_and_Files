?	tF??_??tF??_??!tF??_??	???^F6@???^F6@!???^F6@"e
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails$tF??_??o??ʡ??AǺ????Y?f??j+??*	effff{@2F
Iterator::Model]?C?????!?Ua??V@)??HP??1?g???U@:Preprocessing2l
5Iterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat??d?`T??!???	?@)?ZӼ???1??ڟE
@:Preprocessing2v
?Iterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::ConcatenateHP?sג?!??
br@)??Pk?w??1?=Ӥ??	@:Preprocessing2U
Iterator::Model::ParallelMapV2??~j?t??!??S???@)??~j?t??1??S???@:Preprocessing2Z
#Iterator::Model::ParallelMapV2::Zipj?t???!?W???#@)a2U0*?s?1h?????:Preprocessing2?
OIterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate[0]::TensorSlice;?O??nr?!r?>????);?O??nr?1r?>????:Preprocessing2x
AIterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat::FromTensor???_vOn?!?Y?D?a??)???_vOn?1?Y?D?a??:Preprocessing2f
/Iterator::Model::ParallelMapV2::Zip[0]::FlatMapDio??ɔ?!
tƊf?@)ŏ1w-!_?1e???B??:Preprocessing:?
]Enqueuing data: you may want to combine small input data chunks into fewer but larger chunks.
?Data preprocessing: you may increase num_parallel_calls in <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#map" target="_blank">Dataset map()</a> or preprocess the data OFFLINE.
?Reading data from files in advance: you may tune parameters in the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch size</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave cycle_length</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer_size</a>)
?Reading data from files on demand: you should read data IN ADVANCE using the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer</a>)
?Other data reading or processing: you may consider using the <a href="https://www.tensorflow.org/programmers_guide/datasets" target="_blank">tf.data API</a> (if you are not using it now)?
:type.googleapis.com/tensorflow.profiler.BottleneckAnalysis?
host?Your program is HIGHLY input-bound because 22.3% of the total step time sampled is waiting for input. Therefore, you should first focus on reducing the input time.no*high2t40.2 % of the total step time sampled is spent on 'All Others' time. This could be due to Python execution overhead.9???^F6@>Look at Section 3 for the breakdown of input time on the host.B?
@type.googleapis.com/tensorflow.profiler.GenericStepTimeBreakdown?
	o??ʡ??o??ʡ??!o??ʡ??      ??!       "      ??!       *      ??!       2	Ǻ????Ǻ????!Ǻ????:      ??!       B      ??!       J	?f??j+???f??j+??!?f??j+??R      ??!       Z	?f??j+???f??j+??!?f??j+??JCPU_ONLYY???^F6@b Y      Y@q?A?J?O@"?	
host?Your program is HIGHLY input-bound because 22.3% of the total step time sampled is waiting for input. Therefore, you should first focus on reducing the input time.b
`input_pipeline_analyzer (especially Section 3 for the breakdown of input operations on the Host)m
ktrace_viewer (look at the activities on the timeline of each Host Thread near the bottom of the trace view)"T
Rtensorflow_stats (identify the time-consuming operations executed on the CPU_ONLY)"Z
Xtrace_viewer (look at the activities on the timeline of each CPU_ONLY in the trace view)*?
?<a href="https://www.tensorflow.org/guide/data_performance_analysis" target="_blank">Analyze tf.data performance with the TF Profiler</a>*y
w<a href="https://www.tensorflow.org/guide/data_performance" target="_blank">Better performance with the tf.data API</a>2?
=type.googleapis.com/tensorflow.profiler.GenericRecommendation?
nohigh"t40.2 % of the total step time sampled is spent on 'All Others' time. This could be due to Python execution overhead.:
Refer to the TF2 Profiler FAQb?63.7757% of Op time on the host used eager execution. Performance could be improved with <a href="https://www.tensorflow.org/guide/function" target="_blank">tf.function.</a>2"CPU: B 