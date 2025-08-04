#pragma once

#ifdef __GNUC__
#define NTT_ANNOTATE(annotation) __attribute__((annotate(annotation)))
#else
#define NTT_ANNOTATE(annotation)
#endif

#define NTT_SINGLETON NTT_ANNOTATE("singleton")
#define NTT_PYTHON_BINDING NTT_ANNOTATE("python")
