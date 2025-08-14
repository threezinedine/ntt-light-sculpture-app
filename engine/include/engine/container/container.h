#pragma once
#include "engine/common/common.h"

namespace NTT_NS
{
    template <typename T>
    using ContainerAllocator = std::function<T *(void *)>;

    template <typename T>
    using ContainerDeallocator = std::function<void(T *)>;

    /**
     * General storage for all type T pointers, user can retrieve, insert, delete with the data objects via the
     *      id of that object.
     */
    template <typename T>
    class Container
    {
    public:
        Container(ContainerAllocator<T> allocator, ContainerDeallocator<T> deallocator, u32 maxCount = MAX_CONTAINER_OBJECTS)
            : m_allocator(allocator), m_deallocator(deallocator), m_largestObjectId(0)
        {
            m_objects.resize(maxCount);
            memset(m_objects.data(), 0, sizeof(T *) * maxCount);
        }

        Container(const Container &) = delete;

        ~Container()
        {
            for (u32 objectId = 0; objectId < m_largestObjectId; ++objectId)
            {
                T *object = m_objects[objectId];
                if (object != nullptr)
                {
                    m_deallocator(object);
                }
            }
        }

        u32 Create(void *data = nullptr)
        {
            if (!m_freeIds.empty())
            {
                T *object = m_allocator(data);
                u32 id = *m_freeIds.begin();
                m_freeIds.erase(m_freeIds.begin());
                m_objects[id] = object;
                return id;
            }
            else if (m_largestObjectId < m_objects.size())
            {
                T *object = m_allocator(data);
                m_objects[m_largestObjectId++] = object;
                return m_largestObjectId - 1; // Return the index as ID
            }

            return INVALID_ID;
        }

        void Destroy(u32 id)
        {
            T *object = m_objects[id];
            if (object != nullptr)
            {
                m_deallocator(object);
                m_objects[id] = nullptr; // Mark as deleted
                m_freeIds.insert(id);
            }
            else
            {
                char errorBuffer[ERROR_BUFFER_SIZE];
                snprintf(errorBuffer, sizeof(errorBuffer), "Invalid object ID: %u", id);
                throw std::out_of_range(errorBuffer);
            }
        }

        inline T *Get(u32 id) const { return m_objects[id]; }
        inline bool IsValidId(u32 id) const { return m_objects[id] != nullptr; }

    private:
        ContainerAllocator<T> m_allocator;     // Function to create a new object of type T
        ContainerDeallocator<T> m_deallocator; // Function to release an object of type T

        vector<T *> m_objects; // Map to store objects with their IDs

        /**
         * Store the reference for the next available object ID
         *      it also represents the current used size of the container
         */
        u32 m_largestObjectId = 0;

        set<u32> m_freeIds; // Set of free object IDs
    };
} // namespace NTT_NS