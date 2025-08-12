#pragma once
#include "engine/common/common.h"

namespace NTT_NS
{
    /**
     * Simple interface to opengl shader programming. User can easy to attach this program for using in the next rendering block.
     *
     * @example
     * ```c++
     * Program program(vertexShaderSource, fragmentShaderSource);
     * program.Compile();
     *
     * // Start the
     * program.Use();
     *
     * // drawing code block
     * ```
     */
    class Program
    {
    public:
        Program();
        /**
         * At the start, no working process is attached to the program. No compile, must call `Compile()` method
         *      for creating the program.
         *
         * @param vertexShader Vertex shader source code which will be affected for each vertex.
         * @param fragmentShader Fragment shader source code which will be affected for each fragment.
         */
        Program(string vertexShader, string fragmentShader);
        ~Program();

        inline void AddVertexShader(string vertexShader) { m_vertexShaderSource = vertexShader; };
        inline void AddFragmentShader(string fragmentShader) { m_fragmentShaderSource = fragmentShader; };

        /**
         * Should be called once for each session (usually in `Intialization`), the program will be created and error
         *      check.
         *
         * If compilation fails, an error will be thrown.
         */
        void Compile();

        /**
         * The main method of the current class which will attach this program into the rendering pipeline. When
         *      a new program is used, then the previous program will be released automatically.
         */
        void Use();

    private:
        void CompileShader(u32 shaderId, const char *shaderSource);

    private:
        u32 m_programID = 0;
        string m_vertexShaderSource = "";
        string m_fragmentShaderSource = "";
    };
}