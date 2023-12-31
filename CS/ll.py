#!/usr/bin/env python38
#-*- coding:utf-8 -*-
import flink.plan.Environment



def hello_world():
    """
    从随机Source读取数据，然后直接利用PrintSink输出。
    """
    settings = EnvironmentSettings.new_instance().in_streaming_mode().use_blink_planner().build()
    env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(stream_execution_environment=env, environment_settings=settings)
    source_ddl = """
                    CREATE TABLE random_source (
                        f_sequence INT,
                        f_random INT,
                        f_random_str STRING
                    ) WITH (
                        'connector' = 'datagen',
                        'rows-per-second'='5',
                        'fields.f_sequence.kind'='sequence',
                        'fields.f_sequence.start'='1',
                        'fields.f_sequence.end'='1000',
                        'fields.f_random.min'='1',
                        'fields.f_random.max'='1000',
                        'fields.f_random_str.length'='10'
                    )
                    """

    sink_ddl = """
                  CREATE TABLE print_sink (
                    f_sequence INT,
                    f_random INT,
                    f_random_str STRING 
                ) WITH (
                  'connector' = 'print'
                )
        """

    # 注册source和sink
    t_env.execute_sql(source_ddl)
    t_env.execute_sql(sink_ddl)

    # 数据提取
    tab = t_env.from_path("random_source")
    # 这里我们暂时先使用 标注了 deprecated 的API, 因为新的异步提交测试有待改进...
    tab.execute_insert("print_sink").wait()
    # 执行作业
    t_env.execute_sql("Flink Hello World")



if __name__ == '__main__':
    hello_world()
