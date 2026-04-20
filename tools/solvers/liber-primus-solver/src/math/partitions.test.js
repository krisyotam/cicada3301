import {Partitions} from './partitions'

it('can find the correct closest numbers to the left of the given ones', () => {
    const sut = new Partitions()

    expect(sut.nearestNumberToTheLeft(1)).toEqual(null)
    expect(sut.nearestNumberToTheLeft(300)).toEqual(109)

    expect(sut.nearestNumberToTheLeft(6)).toEqual(5)
    expect(sut.nearestNumberToTheLeft(108)).toEqual(107)
    expect(sut.nearestNumberToTheLeft(53)).toEqual(47)

})

it('can compute partitions', () => {
    const sut = new Partitions()

    expect(sut.computePartitions(5)).toEqual([[3, 2]])
    expect(sut.computePartitions(6)).toEqual([[3, 3], [2, 2, 2]])
    expect(sut.computePartitions(8)).toEqual([[5, 3], [3, 3, 2], [2, 2, 2, 2]])
    expect(sut.computePartitions(11)).toEqual([[7, 2, 2], [5, 3, 3], [5, 2, 2, 2], [3, 3, 3, 2], [3, 2, 2, 2, 2]])

})

