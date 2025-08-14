#pragma once

#ifdef __GNUC__
#define NTT_ANNOTATE(annotation) __attribute__((annotate(annotation)))
#else
#define NTT_ANNOTATE(annotation)
#endif

#define NTT_SINGLETON NTT_ANNOTATE("singleton")

/**
 * Be used for marking that the target can be accessed from Python. With this
 *      macro, the `autogen` module can identify the target and generate the
 *      appropriate bindings.
 *
 * @note This binding macro cannot be used with inline method which define inside the code,
 *      must separate the definition and declaration.
 */
#define NTT_PYTHON_BINDING NTT_ANNOTATE("python")
