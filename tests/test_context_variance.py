import numpy
import context
import vigra
from numpy.testing import assert_equal, assert_almost_equal

def testVariance2D():
    #test computation of variance features. average features are computed along the way
    #but not tested here
    #
    #!!! this test assumes that there are only 2 neighborhood sizes !!!

    nx = 7
    ny = 10
    nc = 2
    dummypred = numpy.random.rand(nx, ny, nc)
    #dummypred = numpy.arange(nx*ny*nc)
    dummypred = dummypred.reshape((nx, ny, nc))
    dummypred = dummypred.astype(numpy.float32)

    dummy = vigra.VigraArray(dummypred.shape, axistags=vigra.VigraArray.defaultAxistags(3)).astype(dummypred.dtype)
    dummy[:]=dummypred[:]

    #print dummypred[:, :, 0]

    sizes = numpy.array([1, 2], dtype=numpy.uint32)
    nr = sizes.shape[0]
    resshape = (nx, ny, nc*2*sizes.shape[0])
    res = vigra.VigraArray(resshape, axistags=vigra.VigraArray.defaultAxistags(3)).astype(numpy.float32)

    res = context.varContext2Dmulti(sizes, dummy, res)

    #test simple variance
    var11_0 = numpy.var(dummypred[0:3, 0:3, 0])
    var11_1 = numpy.var(dummypred[0:3, 0:3, 1])
    if (abs(var11_0-res[1, 1, nr])>1E-5 or abs(var11_1-res[1, 1, 2*nr+nr])>1E-5):
        print "variance x 1, y 1, c 0:", var11_0, ", computed as:", res[1, 1, nr]
        print "variance x 1, y 1, c 1:", var11_1, ", computed as:", res[1, 1, 2*nr+nr]
        
    var22_0 = numpy.var(dummypred[1:4, 1:4, 0])
    var22_1 = numpy.var(dummypred[1:4, 1:4, 1])
    if (abs(var22_0-res[2, 2, nr])>1E-5 or abs(var22_1-res[2, 2, 2*nr+nr])>1E-5):
        print "variance x 2, y 2, c 0:", var22_0, ", computed as:", res[2, 2, nr]
        print "variance x 2, y 2, c 1:", var22_1, ", computed as:", res[2, 2, 2*nr+nr]
        
    #test variance of rectangles without middle
    rec22 = [dummypred[0, 0, 0], dummypred[0, 1, 0], dummypred[0, 2, 0], dummypred[0, 3, 0], dummypred[0, 4, 0]]
    rec22.extend([dummypred[1, 0, 0], dummypred[2, 0, 0], dummypred[3, 0, 0], dummypred[4, 0, 0]])
    rec22.extend([dummypred[4, 1, 0], dummypred[4, 2, 0], dummypred[4, 3, 0], dummypred[4, 4, 0]])
    rec22.extend([dummypred[3, 4, 0], dummypred[2, 4, 0], dummypred[1, 4, 0]])

    rec22arr = numpy.array(rec22)
    var22_0_2 = numpy.var(rec22arr)
    if (abs(var22_0_2-res[2, 2, nr+1]>1E-5)):
        print "variance x2, y2, c0, r=2:", var22_0_2, "computed as:", res[2, 2, nr+1]

def testVariance3D():
    #test variance computation in 3D
    nx = 7
    ny = 10
    nz = 7
    nc = 2
    
    dummypred = numpy.ones(nx*ny*nz*nc)
    #dummypred = numpy.random.rand(nx, ny, nz, nc)
    dummypred = dummypred.reshape((nx, ny, nz, nc))
    dummypred = dummypred.astype(numpy.float32)
    dummy = vigra.VigraArray(dummypred.shape, axistags=vigra.VigraArray.defaultAxistags(4)).astype(dummypred.dtype)
    dummy[:]=dummypred[:]

    #just one radius and test against numpy variance
    sizes = numpy.array([2, 3], dtype=numpy.uint32)
    nr = sizes.shape[0]
    resshape = (nx, ny, nz, nc*2*sizes.shape[0])
    res = vigra.VigraArray(resshape, axistags=vigra.VigraArray.defaultAxistags(4)).astype(numpy.float32)

    res = context.varContext3Dmulti(sizes, dummy, res)
    
    #test the first radius, we should have just average and variance for it
    for x in range(sizes[0], nx-sizes[0]):
        for y in range(sizes[0], ny-sizes[0]):
            for z in range(sizes[0], nz-sizes[0]):
                for c in range(nc):
                    temp = dummy[x-sizes[0]:x+sizes[0]+1, y-sizes[0]:y+sizes[0]+1, z-sizes[0]:z+sizes[0]+1, c]
                    #print x, y, z
                    m = numpy.mean(temp)
                    assert_almost_equal(m, res[x, y, z, c*2*nr], 1)
                    v = numpy.var(temp)
                    assert_almost_equal(v, res[x, y, z, c*2*nr+nr], 1)
                    
    for x in range(sizes[1], nx-sizes[1]):
        for y in range(sizes[1], ny-sizes[1]):
            for z in range(sizes[1], nz-sizes[1]):
                for c in range(nc):
                    temp_out = dummy[x-sizes[1]:x+sizes[1]+1, y-sizes[1]:y+sizes[1]+1, z-sizes[1]:z+sizes[1]+1, c]
                    temp_in = dummy[x-sizes[0]:x+sizes[0]+1, y-sizes[0]:y+sizes[0]+1, z-sizes[0]:z+sizes[0]+1, c]
                    
                    sum_out = numpy.sum(temp_out)
                    sum_in = numpy.sum(temp_in)
                    summ = sum_out - sum_in
                    m = summ/(temp_out.size - temp_in.size)
                    assert_almost_equal(m, res[x, y, z, c*2*nr+1], 1)
                    #v = numpy.var(temp)
                    #assert_almost_equal(v, res[x, y, z, c*2*nr+nr], 1)
    

    


if __name__=="__main__":
    #testVariance2D();
    testVariance3D();
    

