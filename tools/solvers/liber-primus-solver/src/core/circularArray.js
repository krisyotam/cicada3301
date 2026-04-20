export class CircularArray {
    constructor(array) {
        this.array = array
        this.currentIndex = 0
        this.mod = this.array.length
    }

    next = () => {
        const nextElement = this.array[this.currentIndex]

        this.currentIndex = (++this.currentIndex) % this.mod

        return nextElement
    }
}
