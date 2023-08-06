import renderapi
from .utils import (
        AlignerTransformException,
        ptpair_indices,
        arrays_for_tilepair)
import numpy as np
import scipy.sparse as sparse


class AlignerRigidModel(renderapi.transform.AffineModel):

    def __init__(self, transform=None):

        if transform is not None:
            if isinstance(transform, renderapi.transform.AffineModel):
                self.from_dict(transform.to_dict())
            else:
                raise AlignerTransformException(
                        "can't initialize %s with %s" % (
                            self.__class__, transform.__class__))
        else:
            self.from_dict(renderapi.transform.AffineModel().to_dict())

        self.DOF_per_tile = 3
        self.nnz_per_row = 4
        self.rows_per_ptmatch = 3

    def to_solve_vec(self, input_tform):
        if isinstance(input_tform, renderapi.transform.AffineModel):
            approx_tform = input_tform
        elif isinstance(
                input_tform, renderapi.transform.Polynomial2DTransform):
            approx_tform = renderapi.transform.AffineModel(
                    M00=input_tform.params[0, 1],
                    M01=input_tform.params[0, 2],
                    B0=input_tform.params[0, 0],
                    M10=input_tform.params[1, 1],
                    M11=input_tform.params[1, 2],
                    B1=input_tform.params[1, 0])
        else:
            raise AlignerTransformException(
                    "no method to represent input tform %s in solve as %s" % (
                        input_tform.__class__, self.__class__))

        vec = np.array([
            approx_tform.M[0, 2],
            approx_tform.M[1, 2],
            approx_tform.rotation])
        vec = vec.reshape((vec.size, 1))
        return vec

    def from_solve_vec(self, vec):
        tforms = []
        n = int(vec.shape[0] / 3)
        for i in range(n):
            theta = vec[i * 3 + 2]
            self.M[0, 0] = np.cos(theta)
            self.M[0, 1] = -np.sin(theta)
            self.M[1, 0] = np.sin(theta)
            self.M[1, 1] = np.sin(theta)
            self.M[0, 2] = vec[i * 3 + 0]
            self.M[1, 2] = vec[i * 3 + 1]
            tforms.append(
                    renderapi.transform.AffineModel(
                        json=self.to_dict()))
        return tforms

    def create_regularization(self, sz, regdict):
        reg = np.ones(sz).astype('float64') * regdict['default_lambda']
        reg[0::3] *= regdict['translation_factor']
        reg[1::3] *= regdict['translation_factor']
        outr = sparse.eye(reg.size, format='csr')
        outr.data = reg
        return outr

    def CSR_from_tilepair(
            self, match, tile_ind1, tile_ind2,
            nmin, nmax, choose_random):
        if np.all(np.array(match['matches']['w']) == 0):
            # zero weights
            return None, None, None, None, None

        match_index, stride = ptpair_indices(
                len(match['matches']['q'][0]),
                nmin,
                nmax,
                self.nnz_per_row,
                choose_random)
        if match_index is None:
            # did not meet nmin requirement
            return None, None, None, None, None

        npts = match_index.size

        # empty arrays
        data, indices, indptr, weights = (
                arrays_for_tilepair(
                        npts,
                        self.rows_per_ptmatch,
                        self.nnz_per_row))

        px = np.array(match['matches']['p'][0])[match_index]
        px -= px.mean()
        py = np.array(match['matches']['p'][1])[match_index]
        py -= py.mean()
        qx = np.array(match['matches']['q'][0])[match_index]
        qx -= qx.mean()
        qy = np.array(match['matches']['q'][1])[match_index]
        qy -= qy.mean()

        ptheta = np.arctan2(py, px)
        qtheta = np.arctan2(qy, qx)

        # px_com + pdx = qx_com + qdx
        data[0 + stride] = px
        data[1 + stride] = 1.0
        data[2 + stride] = -1.0 * qx
        data[3 + stride] = -1.0
        uindices = np.hstack((
            tile_ind1 * self.DOF_per_tile + np.array([0, 1]),
            tile_ind2 * self.DOF_per_tile + np.array([0, 1])))
        indices[0: npts * self.nnz_per_row] = np.tile(uindices, npts)
        # py_com + pdy = qy_com + qdy
        data[0 + stride + npts * self.nnz_per_row] = py
        data[1 + stride + npts * self.nnz_per_row] = 1.0
        data[2 + stride + npts * self.nnz_per_row] = -1.0 * qy
        data[3 + stride + npts * self.nnz_per_row] = -1.0
        uindices = np.hstack((
            tile_ind1 * self.DOF_per_tile + np.array([0, 1]),
            tile_ind2 * self.DOF_per_tile + np.array([0, 1])))
        indices[0: npts * self.nnz_per_row] = np.tile(uindices, npts)
        # v=-bx+ay+d
        data[0 + stride + npts * self.nnz_per_row] = -1.0 * px
        data[1 + stride + npts * self.nnz_per_row] = py
        data[2 + stride + npts * self.nnz_per_row] = 1.0
        data[3 + stride + npts * self.nnz_per_row] = 1.0 * qx
        data[4 + stride + npts * self.nnz_per_row] = -1.0 * qy
        data[5 + stride + npts * self.nnz_per_row] = -1.0
        vindices = np.hstack((
            tile_ind1 * self.DOF_per_tile + np.array([1, 0, 3]),
            tile_ind2 * self.DOF_per_tile + np.array([1, 0, 3])))
        indices[
                npts*self.nnz_per_row:
                2 * npts * self.nnz_per_row] = np.tile(vindices, npts)
        # du
        data[0 + stride + 2 * npts * self.nnz_per_row] = \
            px - px.mean()
        data[1 + stride + 2 * npts * self.nnz_per_row] = \
            py - py.mean()
        data[2 + stride + 2 * npts * self.nnz_per_row] = \
            0.0
        data[3 + stride + 2 * npts * self.nnz_per_row] = \
            -1.0 * (qx - qx.mean())
        data[4 + stride + 2 * npts * self.nnz_per_row] = \
            -1.0 * (qy - qy.mean())
        data[5 + stride + 2 * npts * self.nnz_per_row] = \
            -0.0
        indices[2 * npts * self.nnz_per_row:
                3 * npts * self.nnz_per_row] = np.tile(uindices, npts)
        # dv
        data[0 + stride + 3 * npts * self.nnz_per_row] = \
            -1.0 * (px - px.mean())
        data[1 + stride + 3 * npts * self.nnz_per_row] = \
            py - py.mean()
        data[2 + stride + 3 * npts * self.nnz_per_row] = \
            0.0
        data[3 + stride + 3 * npts * self.nnz_per_row] = \
            1.0 * (qx - qx.mean())
        data[4 + stride + 3 * npts * self.nnz_per_row] = \
            -1.0 * (qy - qy.mean())
        data[5 + stride + 3 * npts * self.nnz_per_row] = \
            -0.0
        indices[3 * npts * self.nnz_per_row:
                4 * npts * self.nnz_per_row] = np.tile(uindices, npts)

        indptr[0: self.rows_per_ptmatch * npts] = \
            np.arange(1, self.rows_per_ptmatch * npts + 1) * \
            self.nnz_per_row
        weights[0: self.rows_per_ptmatch * npts] = \
            np.tile(np.array(
                match['matches']['w'])[match_index],
                self.rows_per_ptmatch)

        return data, indices, indptr, weights, npts
