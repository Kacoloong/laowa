//
// Created by Rezarc on 2025/3/31.
//

#include "gurobi_c++.h"
#include <bits/stdc++.h>
using namespace std;

namespace Algo {
    const int ROUND = 25;
    const int ROW = 4;
    const int COLUMN = 4;
    const int LANE = 8;
    vector<GRBVar> stateInput[ROUND][ROW][COLUMN][LANE];
    vector<GRBVar> stateSubBytes[ROUND][ROW][COLUMN][LANE];
    vector<GRBVar> stateShiftColumn[ROUND][ROW][COLUMN][LANE];
    vector<GRBVar> stateMixRow[ROUND][ROW][COLUMN][LANE];
    vector<GRBVar> stateLaneTransform[ROUND][ROW][COLUMN][LANE];
    GRBVar flagInput[ROUND][ROW][COLUMN][LANE];
    GRBVar flagSubBytes[ROUND][ROW][COLUMN][LANE];
    GRBVar flagShiftColumn[ROUND][ROW][COLUMN][LANE];
    GRBVar flagMixRow[ROUND][ROW][COLUMN][LANE];
    GRBVar flagLaneTransform[ROUND][ROW][COLUMN][LANE];

    stringstream ss;
    const int p[4] = {3, 2, 1, 2};
    const int M[4][4] = {
        {1, 1, 2, 4},
        {1, 2, 4, 1},
        {2, 4, 1, 1},
        {4, 1, 1, 2}
    };
    const int laneTrans[4][4] = {
        {2, 7, 2, 3},
        {0, 4, 3, 6},
        {4, 3, 1, 4},
        {1, 1, 5, 0}
    };
    int idx = 0;
    void equals(GRBModel &model, GRBVar &a, GRBVar &b) {
        model.addConstr(a == b);
        model.update();
    }
    void MixRow(GRBModel &model, vector<GRBVar> &in, vector<GRBVar> &out) {
        GRBVar auxi = model.addVar(0, 1, 0, GRB_BINARY, "auxi_" + to_string(++ idx));
        GRBLinExpr in_expr = 0, out_expr = 0;
        for (auto &it : in) in_expr += it;
        for (auto &it : out) out_expr += it;
        model.addConstr(in_expr + out_expr - 5 * auxi >= 0);
        model.addConstr(in_expr - auxi >= 0);
        model.addConstr(out_expr - auxi >= 0);
        for (int i = 0; i < 4; i ++) {
            model.addConstr(auxi - in[i] >= 0);
            model.addConstr(auxi - out[i] >= 0);
        }
        model.update();
    }
    void generateVariables(GRBModel &model, int round) {
        for (int r = 0; r <= round; r ++) {
            for (int i = 0; i < ROW; i ++) {
                for (int j = 0; j < COLUMN; j ++) {
                    for (int k = 0; k < LANE; k ++) {
                        stateInput[r][i][j][k].clear();
                        ss << "flagInput" << r << "_" << i << "_" << j << "_" << k;
                        flagInput[r][i][j][k] = (model.addVar(0, 1, 0, GRB_BINARY, ss.str()));
                        ss.str("");
                        for (int b = 0; b < 8; b ++) {
                            ss << "stateInput" << r << "_" << i << "_" << j << "_" << k << "_" << b;
                            stateInput[r][i][j][k].push_back(model.addVar(0, 1, 0, GRB_BINARY, ss.str()));
                            ss.str("");
                        }
                    }
                }
            }
        }
        for (int r = 0; r < round; r ++) {
            for (int i = 0; i < ROW; i ++) {
                for (int j = 0; j < COLUMN; j ++) {
                    for (int k = 0; k < LANE; k ++) {
                        stateSubBytes[r][i][j][k].clear();
                        stateShiftColumn[r][i][j][k].clear();
                        stateMixRow[r][i][j][k].clear();
                        stateLaneTransform[r][i][j][k].clear();
                        ss << "flagSubBytes" << r << "_" << i << "_" << j << "_" << k;
                        flagSubBytes[r][i][j][k] = (model.addVar(0, 1, 0, GRB_BINARY, ss.str()));
                        ss.str("");
                        ss << "flagShiftColumn" << r << "_" << i << "_" << j << "_" << k;
                        flagShiftColumn[r][i][j][k] = (model.addVar(0, 1, 0, GRB_BINARY, ss.str()));
                        ss.str("");
                        ss << "flagMixRow" << r << "_" << i << "_" << j << "_" << k;
                        flagMixRow[r][i][j][k] = (model.addVar(0, 1, 0, GRB_BINARY, ss.str()));
                        ss.str("");
                        ss << "flagLaneTransform" << r << "_" << i << "_" << j << "_" << k;
                        flagLaneTransform[r][i][j][k] = (model.addVar(0, 1, 0, GRB_BINARY, ss.str()));
                        ss.str("");
                        for (int b = 0; b < 8; b ++) {
                            ss << "stateSubBytes" << r << "_" << i << "_" << j << "_" << k << "_" << b;
                            stateSubBytes[r][i][j][k].push_back(model.addVar(0, 1, 0, GRB_BINARY, ss.str()));
                            ss.str("");
                            ss << "stateShiftColumn" << r << "_" << i << "_" << j << "_" << k << "_" << b;
                            stateShiftColumn[r][i][j][k].push_back(model.addVar(0, 1, 0, GRB_BINARY, ss.str()));
                            ss.str("");
                            ss << "stateMixRow" << r << "_" << i << "_" << j << "_" << k << "_" << b;
                            stateMixRow[r][i][j][k].push_back(model.addVar(0, 1, 0, GRB_BINARY, ss.str()));
                            ss.str("");
                            ss << "stateLaneTransform" << r << "_" << i << "_" << j << "_" << k << "_" << b;
                            stateLaneTransform[r][i][j][k].push_back(model.addVar(0, 1, 0, GRB_BINARY, ss.str()));
                            ss.str("");
                        }
                    }
                }
            }
        }
        model.update();
    }
    void setObjective(GRBModel &model, int round) {
        GRBLinExpr expr = 0;
        for (int r = 0; r < round; r ++) {
            for (int i = 0; i < ROW; i ++) {
                for (int j = 0; j < COLUMN; j ++) {
                    for (int k = 0; k < LANE; k ++) {
                        expr += flagInput[r][i][j][k];
                    }
                }
            }
        }
        model.setObjective(expr, GRB_MINIMIZE);
    }
    void setConstraint(GRBModel &model) {
        GRBLinExpr expr = 0;
        for (int i = 0; i < ROW; i ++) {
            for (int j = 0; j < COLUMN; j++) {
                for (int k = 0; k < LANE; k++) {
                    expr += flagInput[0][i][j][k];
                }
            }
        }
        model.addConstr(expr >= 1);
        model.update();
    }
    void makeModel(GRBModel &model, int round) {
        generateVariables(model, round);
        setConstraint(model);
        setObjective(model, round);
        vector<GRBVar> in, out;
        for (int r = 0; r < round; r ++) {
            for (int i = 0; i < 4; i ++) {
                for (int j = 0; j < 4; j ++) {
                    for (int k = 0; k < 8; k ++) {
                        // SubBytes
                        equals(model, flagInput[r][i][j][k], flagSubBytes[r][i][j][k]);
                        // ShiftColumn
                        equals(model, flagSubBytes[r][i][(j + p[i]) % 4][k], flagShiftColumn[r][i][j][k]);
                    }
                }
            }
            for (int k = 0; k < 8; k ++) {
                for (int i = 0; i < 4; i ++) {
                    in.clear(); out.clear();
                    for (int j = 0; j < 4; j ++) {
                        // MixRow
                        in.push_back(flagShiftColumn[r][i][(j + 1) % 4][(k - 1 + 8) % 8]);
                        out.push_back(flagMixRow[r][i][j][k]);
                    }
                    MixRow(model, in, out);
                    in.clear(); out.clear();
                    // LaneTransform
                    for (int j = 0; j < 4; j ++) {
                        equals(model, flagMixRow[r][i][j][(k - laneTrans[j][i] + 8) % 8], flagInput[r + 1][i][j][k]);
                    }
                }
            }
        }
    }

    void setConstraint(GRBModel &model, int r, int pos1, int pos2) {
        for (int i = 0; i < ROW; i ++) {
            for (int j = 0; j < COLUMN; j++) {
                for (int k = 0; k < LANE; k++) {
                    if (pos1 == i + j * 4 + k * 16) model.addConstr(flagInput[0][i][j][k] == 1);
                    else model.addConstr(flagInput[0][i][j][k] == 0);
                    if (pos2 == i + j * 4 + k * 16) model.addConstr(flagInput[r][i][j][k] == 1);
                    else model.addConstr(flagInput[r][i][j][k] == 0);
                }
            }
        }
        model.update();
    }
    void makeModel(GRBModel &model, int round, int pos1, int pos2) {
        generateVariables(model, round);
        setConstraint(model, round, pos1, pos2);
        setObjective(model, round);
        vector<GRBVar> in, out;
        for (int r = 0; r < round; r ++) {
            for (int i = 0; i < 4; i ++) {
                for (int j = 0; j < 4; j ++) {
                    for (int k = 0; k < 8; k ++) {
                        // SubBytes
                        equals(model, flagInput[r][i][j][k], flagSubBytes[r][i][j][k]);
                        // ShiftColumn
                        equals(model, flagSubBytes[r][i][(j + p[i]) % 4][k], flagShiftColumn[r][i][j][k]);
                    }
                }
            }
            for (int k = 0; k < 8; k ++) {
                for (int j = 0; j < 4; j ++) {
                    in.clear(); out.clear();
                    for (int i = 0; i < 4; i ++) {
                        // MixRow
                        in.push_back(flagShiftColumn[r][i][(j + 1) % 4][(k - 1 + 8) % 8]);
                        out.push_back(flagMixRow[r][i][j][k]);
                    }
                    MixRow(model, in, out);
                    in.clear(); out.clear();
                    // LaneTransform
                    for (int i = 0; i < 4; i ++) {
                        equals(model, flagMixRow[r][i][j][(k - laneTrans[j][i] + 8) % 8], flagInput[r + 1][i][j][k]);
                    }
                }
            }
        }
    }

};