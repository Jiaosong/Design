# FreeCADCmd 1.1.3 imports positional .py files instead of executing them as __main__.
# Keep the benchmark implementation conventional while making the runtime entry explicit.
import run_freecad_parametric_benchmark as benchmark

benchmark.main()
