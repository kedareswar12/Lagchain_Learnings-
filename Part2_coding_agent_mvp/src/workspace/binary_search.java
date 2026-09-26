public class BinarySearch {
    /**
     * Performs binary search on a sorted array.
     *
     * @param arr   Sorted array of integers.
     * @param target Value to search for.
     * @return Index of target if found; otherwise -1.
     */
    public static int binarySearch(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }

    // Simple demo
    public static void main(String[] args) {
        int[] data = {1, 3, 5, 7, 9, 11, 13, 15};
        int target = 7;
        int index = binarySearch(data, target);
        System.out.println("Target " + target + " found at index: " + index);
    }
}
