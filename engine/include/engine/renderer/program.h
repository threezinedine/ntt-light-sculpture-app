#pragma once
#include "engine/common/common.h"

namespace NTT_NS
{
    /**
     * Get the shader name by its type.
     */
    void GetShaderNameByType(u32 shaderType, string &outName);

    /**
     * Used for creating shader with a specific type and source code.
     */
    u32 MakeShader(u32 shaderType, const char *shaderSource);

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
        ~Program();

        /**
         * Use with the help of `MakeShader`
         */
        void Append(u32 shaderID);

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

        template <typename T>
        void SetUniform(const string &name, const T &value);

    private:
        u32 m_programID = 0;
        vector<u32> m_shaderIDs; ///< The list of shader IDs which are attached to this program.
    };
}