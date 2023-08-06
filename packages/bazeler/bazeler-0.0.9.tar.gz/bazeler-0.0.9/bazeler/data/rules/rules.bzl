COMMON_OPTS = ["-std=c++14", "-DEIGEN_INITIALIZE_MATRICES_BY_NAN"]
COMPILE_OPTS = COMMON_OPTS + ["-Wall", "-pedantic", "-Wextra", "-Wno-gnu"]
# Ideally:
#  STRICT_OPTS = COMPILE_OPTS + ["-Werror"]
# But this has to be configured on a per-codebase level
STRICT_OPTS = COMPILE_OPTS 

def configs():
    native.config_setting(
          name = "darwin",
          constraint_values = [
             "@bazel_tools//platforms:osx",
             "@bazel_tools//platforms:x86_64"
          ],
          visibility = ["//visibility:public"],
      )

    native.config_setting(
          name = "linux_x86",
          constraint_values = [
             "@bazel_tools//platforms:linux",
             "@bazel_tools//platforms:x86_64"
          ],
          visibility = ["//visibility:public"],
      )

    native.config_setting(
          name = "linux_arm",
          constraint_values = [
             "@bazel_tools//platforms:linux",
             "@bazel_tools//platforms:aarch64"
          ],
          visibility = ["//visibility:public"],
      )
